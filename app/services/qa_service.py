from typing import List
# from langchain_openai import OpenAI
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
# client = OpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")

async def answer_question(question: str, context: str) -> str:
    """
    Uses Langchain to answer a single question based on the provided context.
    """  
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
    print(">>> questions ", questions)
    document = await read_file(document_file, document_file.content_type)
    print(">>> document ", document, "doc type ", type(document))
    questions = [list(d.values())[0] for d in questions]
    print(">>> all questions ", questions)
    if isinstance(questions, str):
        questions = [questions]

    # Answer each question
    answers = []
    for question in questions:
        answer = await answer_question(question, document)
        answers.append({"question": question, "answer": answer})

    return answers
