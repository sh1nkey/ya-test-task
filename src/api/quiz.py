import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db_session
from src.schemas import QuizQuestionDTO, QuizRequest
from src.service.injector import get_question_service
from src.service.quiz import QuestionService

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post(
    "/save-quiz-questions",
    description="Эндпоинт получения вопросов для викторин",
    status_code=201,
    response_description="Список вопросов из англоязычного API викторин",
)
async def save_quiz_quistions(
    req_data: QuizRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    question_service: Annotated[QuestionService, Depends(get_question_service)],
) -> list[QuizQuestionDTO]:
    for _ in range(0, 5):
        questions_to_check = await question_service.get_quiz_data(
            req_data.questions_num
        )
        try:
            await question_service.save_questions(session, questions=questions_to_check)
            return questions_to_check
        except (IntegrityError, PendingRollbackError):
            await asyncio.sleep(1)
            continue
    raise HTTPException(500, "Не удалось получить уникальные вопросы")
