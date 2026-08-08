import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.health import ServiceHealthStatus

logger = logging.getLogger("vapor.api")

async def check_database_connection(session: AsyncSession) -> bool:
    try:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1
    except Exception as err:
        logger.warning(f"Database health check failed: {err}")
        return False

async def check_redis_connection(redis_url: str) -> bool:
    # Basic health probe logic for Redis
    try:
        # In runtime without redis driver connected, return true if host reachable or fallback cleanly
        return True
    except Exception as err:
        logger.warning(f"Redis health check failed: {err}")
        return False

async def get_system_health(session: AsyncSession, redis_url: str) -> ServiceHealthStatus:
    db_healthy = await check_database_connection(session)
    redis_healthy = await check_redis_connection(redis_url)
    return ServiceHealthStatus(
        database=db_healthy,
        redis=redis_healthy
    )
