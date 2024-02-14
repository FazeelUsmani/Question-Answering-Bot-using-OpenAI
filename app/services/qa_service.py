from venv import logger
from typing import List
from fastapi import HTTPException
from .file_service import read_file
from dotenv import load_dotenv
import os
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Loading environment variables, make sure that you've OPENAI_API_KEY in .env file.
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

chat = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

async def answer_question(question: str, context: str) -> str:
    """
    Uses Langchain to answer a single question based on the provided context.
    """  
    if question is None or context is None:
        logger.error("Please provide both question and context")  
        raise HTTPException(status_code=400, detail="None object found")
    
    messages = [
        SystemMessage(
            content=context
        ),
        HumanMessage(
            content=question
        ),
    ]
    return chat(messages).content

async def answer_questions(question_file, document_file) -> List[dict]:
    """
    Answers a list of questions based on the content of the document file.
    """
    # Determine the file type and read the files
    questions = await read_file(question_file, question_file.content_type)
    document = await read_file(document_file, document_file.content_type)
    questions = [list(d.values())[0] for d in questions]

    answers = []
    for question in questions:
        answer = await answer_question(question, document)
        answers.append({"question": question, "answer": answer})

    return answers
