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

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        yield None
        return
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
