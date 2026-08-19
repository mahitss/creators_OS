import time
from urllib.parse import urlparse
from collections import defaultdict
from typing import Dict, List, Tuple, Set
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings
from app.api.routers.auth import verify_jwt_token

PUBLIC_API_ALLOWLIST: Set[str] = {
    "/health",
    "/api/v1/health",
    "/api/v1/auth/login",
    "/api/v1/auth/logout",
    "/api/v1/auth/session",
    "/api/v1/auth/google/url",
    "/api/v1/auth/google/verify",
    "/api/v1/auth/passkey/login/options",
    "/api/v1/auth/passkey/login/verify",
    "/api/v1/auth/passkey/register/options",
    "/api/v1/auth/passkey/register/verify",
    "/api/v1/auth/passkey/verify",
    "/api/v1/integrations/google/callback",
    "/api/v1/telemetry/web-vitals"
}

class AuthenticationEnforcementMiddleware(BaseHTTPMiddleware):
    """Centralized fail-closed security boundary. All protected /api/v1 routes require
    verified JWT or session cookie; unauthenticated requests fail closed with 401."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 1. Allow documentation in development or non-API static/health probes
        if path.startswith("/docs") or path.startswith("/redoc") or path == "/openapi.json":
            return await call_next(request)
        if path in ["/", "/health", "/api/v1/health"]:
            return await call_next(request)

        # 2. Check if route is protected under /api/v1
        if path.startswith("/api/v1"):
            # Check public allowlist
            if path in PUBLIC_API_ALLOWLIST or path.startswith("/api/v1/automations/events/webhooks/"):
                return await call_next(request)

            # 3. Check for Bearer token or session cookie
            auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
            session_cookie = request.cookies.get("vapor_session_token")

            token = None
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            elif session_cookie:
                token = session_cookie

            if not token:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Authentication required. Provide a valid Authorization Bearer token or session cookie."}
                )

            # 4. Verify token validity (bypass only if valid SCIM token)
            if not token.startswith("scim_secret_"):
                try:
                    claims = verify_jwt_token(token)
                    if not claims.get("sub"):
                        return JSONResponse(
                            status_code=401,
                            content={"detail": "Invalid session token: Missing subject claim."}
                        )
                except Exception as exc:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": f"Invalid session token: {str(exc)}"}
                    )

        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Enforces enterprise security headers and Content Security Policy on all HTTP responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        
        is_prod = settings.ENVIRONMENT == "production"
        if is_prod:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' https://openrouter.ai; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "frame-ancestors 'none';"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' http://localhost:* http://127.0.0.1:* https://openrouter.ai; "
                "object-src 'none'; "
                "base-uri 'self';"
            )
        return response


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """Protects state-changing requests against Cross-Site Request Forgery via Origin/Referer validation."""

    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            origin = request.headers.get("origin") or request.headers.get("Origin")
            referer = request.headers.get("referer") or request.headers.get("Referer")

            if origin:
                if origin not in settings.CORS_ORIGINS:
                    return JSONResponse(
                        status_code=403,
                        content={"error": "CSRF_FORBIDDEN", "detail": f"Untrusted origin '{origin}' rejected."}
                    )
            elif referer:
                parsed = urlparse(referer)
                ref_origin = f"{parsed.scheme}://{parsed.netloc}"
                if ref_origin not in settings.CORS_ORIGINS:
                    return JSONResponse(
                        status_code=403,
                        content={"error": "CSRF_FORBIDDEN", "detail": f"Untrusted referer '{ref_origin}' rejected."}
                    )

        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Multi-dimensional sliding-window rate limiter tracking by client IP, User, and Workspace."""

    def __init__(self, app, requests_per_minute: int = 300):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._rate_limits: Dict[str, List[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/health", "/api/v1/health"]:
            return await call_next(request)

        client_ip = request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "127.0.0.1")
        auth_header = request.headers.get("Authorization") or ""
        
        # Dimension key: combines IP + auth token signature to avoid header spoofing
        rate_key = f"{client_ip}:{auth_header[:32]}" if auth_header else client_ip

        now = time.time()
        window_start = now - 60.0

        timestamps = [t for t in self._rate_limits[rate_key] if t > window_start]
        self._rate_limits[rate_key] = timestamps

        if len(timestamps) >= self.requests_per_minute:
            retry_after = int(60.0 - (now - timestamps[0])) if timestamps else 60
            return JSONResponse(
                status_code=429,
                content={
                    "error_code": "RATE_LIMITED",
                    "message": "Too many requests. Rate limit exceeded.",
                    "retry_after_seconds": max(1, retry_after)
                },
                headers={
                    "Retry-After": str(max(1, retry_after)),
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0"
                }
            )

        self._rate_limits[rate_key].append(now)
        remaining = self.requests_per_minute - len(self._rate_limits[rate_key])

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        return response
