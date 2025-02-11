from enum import StrEnum as PyStrEnum
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from src.db.db import Base
from sqlalchemy import DateTime, Enum, String, func, text
from datetime import datetime


class QuestionDifficultyEnum(PyStrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"



class QuestionModel(Base):
    __tablename__: str = "questions"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, index=True, default=uuid4
    )
    difficulty: Mapped[QuestionDifficultyEnum] = mapped_column(Enum(QuestionDifficultyEnum))
    category: Mapped[str] = mapped_column(String(50))
    question: Mapped[str] = mapped_column(unique=True, index=True)
    correct_answer: Mapped[str] = mapped_column(String(40))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, server_default=func.now()
    )
