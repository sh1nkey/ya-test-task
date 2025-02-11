
import pytest_asyncio
from tests.get_db_test import test_engine
from src.db.db import Base, get_db_session
from loguru import logger
from httpx import ASGITransport, AsyncClient
from src.main import app
from tests.get_db_test import get_test_db_session

@pytest_asyncio.fixture
async def setup_db() :
    """ Создание миграций для локальной БД """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info('Запускаем тестовые миграции')

    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # Очистка таблиц


@pytest_asyncio.fixture()
async def ac(setup_db):
    """ Создание тестового клиента """
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        app.dependency_overrides[get_db_session] = get_test_db_session
        yield ac



