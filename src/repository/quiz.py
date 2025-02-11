from typing import Any, override


from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import QuizQuestionDTO
from src.utils.abstract_repo import IPostgresRepo


class QuestionRepo(IPostgresRepo):
    @override
    @classmethod
    async def save_question_data(
        cls,
        connection: AsyncSession,
        *,
        questions: list[QuizQuestionDTO],
        **kwargs: Any,
    ) -> None:
        for question in questions:
            connection.add(question.to_model())
        await connection.commit()
