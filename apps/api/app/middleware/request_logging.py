import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("vapor.api")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time_ms = (time.time() - start_time) * 1000
        logger.info(
            f'{{"method": "{request.method}", "path": "{request.url.path}", '
            f'"status_code": {response.status_code}, "duration_ms": {process_time_ms:.2f}}}'
        )
        response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"
        return response
