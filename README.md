# Question-Answering API with Langchain and OpenAI

This repository contains a backend API for a Question-Answering (QA) bot designed to answer questions based on the content of a document. The bot leverages the capabilities of large language models, utilizing the Langchain framework and OpenAI's gpt-3.5-turbo model.

## Problem Statement

The goal is to create an API that can receive questions and a reference document as inputs and provide accurate answers to the questions using the context provided by the document.

## Suggestions

I'm open for suggestions, how this project can be tweaked to fit in your usecase. For example, to accept .docx or image as input context, search in your order history and so on and so forth. Feel free to contact me.

## Branch

* __main__ - consists OpenAI implementation of this bot
* __langchain__ - consists Langchain implementation of this bot

## Features

* Supports two types of input files: JSON and PDF.
* Answers questions based on the content of the provided document.
* Outputs answers in a structured JSON format.

## Input Requirements

The API requires two input files:

1. A JSON file containing a list of questions.
2. A PDF or JSON file containing the document over which the questions will be answered.

## Output Format

The API returns a JSON list with each question paired with its corresponding answer:

```json
[
    {"question": "What is the name of the company that got audited?", "answer": "Zania"},
    {"question": "What is the name of the pentesting firm?", "answer": "Praveen KSM"},
    ...
]
```

## Technology Requirements

* Python 3.x
* LangChain (Python)
* OpenAI (gpt-3.5-turbo model)
* VectorDB

## Installation

To set up the project, follow these steps:

1. Clone the repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

## Usage

To start the API server, run:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

* `POST /question-answer`: Accepts a multipart/form-data request with `question_file` and `document_file`.

## Sample Input Files

### questions.json

```json
[
    {"1": "What is the name of the company that got audited?"},
    {"2": "What is the name of the pentesting firm?"},
    {"3": "What were the vulnerabilities identified and their severity"}
]
```

### Document (PDF)

The document should be a PDF file containing text that can be extracted and used as context for answering the questions. For example, refer [this pdf](/input_files/zania_pentest_pdf%20(2).pdf)

## Testing

To run the tests, execute:

```bash
pytest tests/
```

## References

1. [https://python.langchain.com/docs/use_cases/question_answering/](https://python.langchain.com/docs/use_cases/question_answering/)
2. [https://python.langchain.com/docs/integrations/chat/openai](https://python.langchain.com/docs/integrations/chat/openai)
