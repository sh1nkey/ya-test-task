from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from typing import Any
from collections.abc import AsyncGenerator
import asyncio

from sqlalchemy.orm import DeclarativeBase
from src.utils.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(settings.postgres.dsn)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
            await asyncio.shield(session.close())
        except Exception:
            await session.rollback()
            raise
        finally:
            await asyncio.shield(session.close())


class Base(DeclarativeBase):
    """Base class for the database models."""
