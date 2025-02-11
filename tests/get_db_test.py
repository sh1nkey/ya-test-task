

import asyncio
from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


TEST_DATABASE_URL = "sqlite+aiosqlite:///mydatabase1.db"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
test_async_session_maker = async_sessionmaker(
    test_engine, 
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_test_db_session() -> AsyncGenerator[Any, Any]:
    async with test_async_session_maker() as session:
        try:
            yield session
            await session.commit()
            await asyncio.shield(session.close())
        except Exception:
            await session.rollback()
            raise
        finally:
            await asyncio.shield(session.close())