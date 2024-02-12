from fastapi import APIRouter, Depends, UploadFile, File
from ..services import qa_service

router = APIRouter()

@router.post("/question-answer")
async def question_answer(question_file: UploadFile = File(...), document_file: UploadFile = File(...)):
    return await qa_service.answer_questions(question_file, document_file)
