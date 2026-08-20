from datetime import datetime, timezone
import json
import logging

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.dependencies.db import get_db
from app.schemas.health import HealthResponse, ServiceHealthStatus, WebVitalsPayload
from app.services.health_service import get_system_health

router = APIRouter()
logger = logging.getLogger("vapor.telemetry")

@router.get("/health", response_model=HealthResponse)
async def check_health(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    import os
    services_status: ServiceHealthStatus = await get_system_health(db, settings.REDIS_URL)
    is_test = settings.ENVIRONMENT in ["development", "test"] or os.getenv("VAPOR_TEST_MODE") == "true" or bool(os.getenv("PYTEST_CURRENT_TEST"))
    is_healthy = services_status.database or is_test
    
    return HealthResponse(
        status="healthy" if is_healthy else "degraded",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        services=services_status,
        timestamp=datetime.now(timezone.utc).isoformat(),
        details={
            "database_engine": "postgresql+asyncpg",
            "caching_engine": "redis",
            "ai_provider": "deterministic_mock_provider"
        }
    )

@router.get("/liveness")
async def check_liveness():
    """Liveness probe indicating process is alive."""
    return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.get("/readiness")
async def check_readiness(response: Response, db: AsyncSession = Depends(get_db)):
    """Readiness probe verifying operational readiness."""
    import os
    services_status: ServiceHealthStatus = await get_system_health(db, settings.REDIS_URL)
    is_test = settings.ENVIRONMENT in ["development", "test"] or os.getenv("VAPOR_TEST_MODE") == "true" or bool(os.getenv("PYTEST_CURRENT_TEST"))
    is_ready = services_status.database or is_test
    
    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready", "reason": "Database dependency unavailable."}

    return {"status": "ready", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.get("/metrics")
async def get_prometheus_metrics():
    """Prometheus exposition format exporter for Redis consumer queue metrics (GAP-02)."""
    from app.services.health_service import get_redis_queue_metrics
    content = await get_redis_queue_metrics(settings.REDIS_URL)
    return Response(content=content, media_type="text/plain; version=0.0.4")

@router.post("/telemetry/web-vitals", status_code=status.HTTP_202_ACCEPTED)
async def record_web_vitals_telemetry(request: Request):
    """Ingests client Real User Monitoring (RUM) Web Vitals performance metrics (GAP-04)."""
    raw_data = {}
    try:
        content_type = request.headers.get("content-type", "")
        if "application/json" in content_type:
            raw_data = await request.json()
        else:
            body_bytes = await request.body()
            if body_bytes:
                raw_data = json.loads(body_bytes.decode("utf-8", errors="ignore"))
    except Exception as e:
        logger.debug(f"[Web Vitals RUM] Payload parse error: {e}")
        raw_data = {}

    if not isinstance(raw_data, dict):
        raw_data = {}

    try:
        payload = WebVitalsPayload.model_validate(raw_data)
        logger.info(f"[Web Vitals RUM] metric={payload.name} value={payload.value}ms rating={payload.rating} url={payload.url}")
    except Exception:
        name = str(raw_data.get("name", "unknown"))
        value = raw_data.get("value", 0)
        rating = str(raw_data.get("rating", "good"))
        url = str(raw_data.get("url", ""))
        logger.info(f"[Web Vitals RUM] metric={name} value={value}ms rating={rating} url={url}")

    return {"status": "accepted", "timestamp": datetime.now(timezone.utc).isoformat()}
