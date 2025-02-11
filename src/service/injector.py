from src.repository.quiz import QuestionRepo
from src.service.quiz import QuestionService, TestQuestionService


def get_question_service() -> QuestionService:
    return QuestionService(QuestionRepo)


def get_test_question_service() -> TestQuestionService:
    return TestQuestionService(QuestionRepo)