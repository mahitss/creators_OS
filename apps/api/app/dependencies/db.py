from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from packages.database.session import AsyncSessionLocal, AsyncSessionTracer

async def get_db() -> AsyncGenerator[AsyncSession, None]:
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

