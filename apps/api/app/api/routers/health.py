from datetime import datetime, timezone
from fastapi import APIRouter, Depends
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
            "caching_engine": "redis"
        }
    )
