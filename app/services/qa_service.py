from typing import List
from langchain.llms import OpenAI
from .file_service import read_file

# Initialize the OpenAI LLM with Langchain
# Ensure that you have set the OPENAI_API_KEY environment variable or pass it explicitly
llm = OpenAI(model="gpt-3.5-turbo")

async def answer_question(question: str, context: str) -> str:
    """
    Uses Langchain to answer a single question based on the provided context.
    """
    response = llm.ask(question, context)
    print(">>> answer question response ", response)
    print(">>> picking this resp", response['choices'][0]['text'].strip())
    return response['choices'][0]['text'].strip()

async def answer_questions(question_file, document_file) -> List[dict]:
    """
    Answers a list of questions based on the content of the document file.
    """
    # Determine the file type and read the files
    questions = await read_file(question_file, question_file.content_type)
    document = await read_file(document_file, document_file.content_type)

    # If the questions are not a list but a single question, wrap it in a list
    if isinstance(questions, str):
        questions = [questions]

    # Answer each question
    answers = []
    for question in questions:
        answer = await answer_question(question, document)
        answers.append({"question": question, "answer": answer})

    return answers
