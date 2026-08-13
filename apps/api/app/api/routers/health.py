from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.dependencies.db import get_db
from app.schemas.health import HealthResponse, ServiceHealthStatus
from app.services.health_service import get_system_health

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def check_health(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    services_status: ServiceHealthStatus = await get_system_health(db, settings.REDIS_URL)
    is_healthy = services_status.database or settings.ENVIRONMENT == "development"
    
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
    services_status: ServiceHealthStatus = await get_system_health(db, settings.REDIS_URL)
    is_ready = services_status.database or settings.ENVIRONMENT == "development"
    
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

