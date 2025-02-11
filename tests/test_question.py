
from httpx import AsyncClient
import pytest
from loguru import logger
from src.service.injector import get_question_service, get_test_question_service
from tests.fixtures import setup_db, ac
from src.main import app

@pytest.mark.asyncio
async def test_get_question_should_succeed(ac: AsyncClient) -> None:
    response = await ac.post("/quiz/save-quiz-questions", json={"questions_num": 10})
    assert response.status_code == 201, response.text
    logger.success(f'Тест успешно проведён! Вот вывод: {response.content}')




@pytest.mark.asyncio
async def test_get_question_should_fail(ac: AsyncClient) -> None:
    """ Идёт 5 секунд тест за счёт ретраев """
    app.dependency_overrides[get_question_service] = get_test_question_service 
    
    # чтобы появилось в БД
    response = await ac.post("/quiz/save-quiz-questions", json={"questions_num": 1})

    
    response = await ac.post("/quiz/save-quiz-questions", json={"questions_num": 1})

    response_data = response.json()

    assert response.status_code == 500, response.text
    assert response_data == {"detail":"Не удалось получить уникальные вопросы"}, response.content

    logger.success(f'Тест успешно проведён! Вот вывод: {response_data}')
