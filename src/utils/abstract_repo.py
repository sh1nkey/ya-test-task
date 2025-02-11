from abc import abstractmethod
from typing import Any, Protocol

from src.schemas import QuizQuestionDTO


class IQuizRepo(Protocol):
    """
    Общий набор методов,
    который должен реализовывать репозиторий quiz
    """

    @classmethod
    @abstractmethod
    async def save_question_data(
        cls, connection: Any, *, questions: list[QuizQuestionDTO], **kwargs: Any
    ) -> None:
        """
        Сохраняет вопрос в БД

        Если есть похожий вопрос - выбрасывает ошибку.
        Её мы обработаем в QuestionService
        """


class IPostgresRepo(IQuizRepo): ...
