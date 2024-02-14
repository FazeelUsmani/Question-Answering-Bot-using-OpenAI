from typing import List
from venv import logger

from fastapi import HTTPException
from .file_service import read_file
from dotenv import load_dotenv
import os
from openai import OpenAI

# Loading environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=openai_api_key)

async def answer_question(question: str, context: str) -> str:
    """
    Uses openai to answer a single question based on the provided context.
    """  
    if question is None or context is None:
        logger.error("Please provide both question and context")  
        raise HTTPException(status_code=400, detail="None object found")
    
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                messages = [
                    {'role': 'system', 'content': context},
                    {'role': 'user', 'content': question}],
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5)
    return response.choices[0].message.content.strip()

async def answer_questions(question_file, document_file) -> List[dict]:
    """
    Answers a list of questions based on the content of the document file.
    """
    # Determine the file type and read the files
    questions = await read_file(question_file, question_file.content_type)
    document = await read_file(document_file, document_file.content_type)
    questions = [list(d.values())[0] for d in questions]

    if isinstance(questions, str):
        questions = [questions]

    answers = []
    for question in questions:
        answer = await answer_question(question, document)
        answers.append({"question": question, "answer": answer})

    return answers
