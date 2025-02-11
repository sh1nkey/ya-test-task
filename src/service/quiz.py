import asyncio
from typing import Any

from sqlalchemy.exc import IntegrityError
from src.schemas import QuizQuestionDTO

from src.utils.abstract_repo import IQuizRepo
import aiohttp
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class QuestionService:
    def __init__(self, quiz_repo: type[IQuizRepo]) -> None:
        self._quiz_repo: type[IQuizRepo] = quiz_repo

    @staticmethod
    async def get_quiz_data(num: int) -> list[QuizQuestionDTO]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"https://opentdb.com/api.php?amount={num}")

            if not response.ok:
                raise HTTPException(
                    500,
                    f"Ошибка при запросе на API викторин. Статус-код: {response.status}. Ответ: {response.text}",
                )

            assert response.status == 200, (
                f"Почему-то ответ у API не 200, а {response.status}"
            )

            response_data: dict[str, Any] = await response.json()

            return [
                QuizQuestionDTO(**question) for question in response_data["results"]
            ]

    async def save_questions(
        self, session: AsyncSession, *, questions: list[QuizQuestionDTO]
    ) -> None:
        await self._quiz_repo.save_question_data(session, questions=questions)


class TestQuestionService(QuestionService):


    @staticmethod
    async def get_quiz_data(num: int) -> list[QuizQuestionDTO]:
        test_data = QuizQuestionDTO(
           difficulty='easy',
           question='who?',
           correct_answer='me',
           category='random'
        )
        return [test_data]
  
        
