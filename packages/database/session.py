import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = logging.getLogger("vapor.database")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///:memory:"
)

try:
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
except Exception as err:
    logger.warning(f"Async database driver init deferred ({err}).")
    engine = None

if engine is not None:
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
else:
    AsyncSessionLocal = None

class AsyncSessionTracer:
    """OpenTelemetry-compatible Async Database Query Span Tracer (GAP-01)."""
    def __init__(self, session: AsyncSession = None, request_id: str = None, trace_id: str = None):
        self.session = session
        self.request_id = request_id or "req_internal_db"
        self.trace_id = trace_id or "tr_internal_db"
        self.span_data = {
            "db.system": "postgresql",
            "db.session": str(id(session)) if session else "none",
            "requestId": self.request_id,
            "traceId": self.trace_id,
            "status": "ACTIVE"
        }

    async def __aenter__(self):
        logger.debug(f"[OTel DB Span Start] requestId={self.request_id} traceId={self.trace_id} db.system=postgresql")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.span_data["status"] = "ERROR"
            logger.error(f"[OTel DB Span Error] requestId={self.request_id} err={exc_val}")
        else:
            self.span_data["status"] = "OK"
            logger.debug(f"[OTel DB Span End] requestId={self.request_id} status=OK")

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        yield None
        return
    async with AsyncSessionLocal() as session:
        async with AsyncSessionTracer(session) as tracer:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

