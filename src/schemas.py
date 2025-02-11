from typing import Literal
from pydantic import BaseModel, PositiveInt

from src.db.models import QuestionModel


class QuizRequest(BaseModel):
    questions_num: PositiveInt


class QuizQuestionDTO(BaseModel):
    difficulty: Literal["easy", "medium", "hard"]
    category: str
    question: str
    correct_answer: str

    def to_model(self) -> QuestionModel:
        """Преобразуем Pydantic модель в модель SqlAlchemy"""
        instance = QuestionModel(
            difficulty=self.difficulty,
            category=self.category,
            question=self.question,
            correct_answer=self.correct_answer,
        )
        return instance
