import time
from urllib.parse import urlparse
from collections import defaultdict
from typing import Dict, List, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Enforces enterprise security headers on all HTTP responses."""

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
    """Protects cookie-authenticated state-changing requests against Cross-Site Request Forgery."""

    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # State-changing requests
            origin = request.headers.get("origin")
            referer = request.headers.get("referer")
            has_cookie = "vapor_session_token" in request.cookies

            # If authenticated by cookie or sending an Origin header, validate the origin
            if origin:
                if origin not in settings.CORS_ORIGINS:
                    return JSONResponse(
                        status_code=403,
                        content={"error": "CSRF_FORBIDDEN", "detail": f"Untrusted origin '{origin}' rejected."}
                    )
            elif referer and has_cookie:
                parsed = urlparse(referer)
                ref_origin = f"{parsed.scheme}://{parsed.netloc}"
                if ref_origin not in settings.CORS_ORIGINS:
                    return JSONResponse(
                        status_code=403,
                        content={"error": "CSRF_FORBIDDEN", "detail": f"Untrusted referer '{ref_origin}' rejected."}
                    )

        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Token-bucket / sliding-window rate limiter per client IP or Auth token."""

    def __init__(self, app, requests_per_minute: int = 300):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._rate_limits: Dict[str, List[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Exclude internal health probes from rate limiting
        if request.url.path in ["/health", "/api/v1/health"]:
            return await call_next(request)

        client_key = request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "127.0.0.1")
        auth_key = request.headers.get("Authorization")
        if auth_key:
            client_key = f"{client_key}:{auth_key}"

        now = time.time()
        window_start = now - 60.0

        # Purge timestamps older than 60s
        timestamps = [t for t in self._rate_limits[client_key] if t > window_start]
        self._rate_limits[client_key] = timestamps

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

        self._rate_limits[client_key].append(now)
        remaining = self.requests_per_minute - len(self._rate_limits[client_key])

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        return response

