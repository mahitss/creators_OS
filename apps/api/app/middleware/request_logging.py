import time
import uuid
import logging
from datetime import datetime, timezone
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

logger = logging.getLogger("vapor.api")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 1. Request ID Generation / Correlation
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id

        # 2. Execute Request Handler
        response = await call_next(request)

        # 3. Calculate Duration & Log Structured JSON
        duration_ms = (time.time() - start_time) * 1000
        now_iso = datetime.now(timezone.utc).isoformat()

        log_payload = {
            "timestamp": now_iso,
            "level": "INFO" if response.status_code < 400 else "ERROR",
            "service": "vapor-api",
            "environment": settings.ENVIRONMENT,
            "requestId": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2)
        }

        logger.info(f"{log_payload}")

        # 4. Attach Request Correlation Headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
        return response
