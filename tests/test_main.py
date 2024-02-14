from fastapi.testclient import TestClient
from app.main import app
import io, json

client = TestClient(app)

def test_question_answer_endpoint():
    # Create a dummy PDF file for testing
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n..."
    pdf_file = io.BytesIO(pdf_content)
    pdf_file.name = 'document.pdf'

    # Create a JSON content
    questions_content = json.dumps([
        {"1": "What is the name of the company that got audited?"},
        {"2": "What is the name of the pentesting firm?"},
        {"3": "What were the vulnerabilities identified and their severity"}
    ])
    questions_file = io.BytesIO(questions_content.encode('utf-8'))
    questions_file.name = 'questions.json'

    # Simulate uploading the files
    response = client.post(
        "/question-answer",
        files={
            "question_file": (questions_file.name, questions_file, "application/json"),
            "document_file": (pdf_file.name, pdf_file, "application/pdf")
        }
    )

    # Validate the response
    assert response.status_code == 200
    answers = response.json()
    assert isinstance(answers, list)
    assert "question" in answers[0]
    assert "answer" in answers[0]


def test_question_answer_invalid_file_type():
    # Create a dummy text file to simulate an unsupported file
    text_content = "This is not a valid input file for the API."
    text_file = io.BytesIO(text_content.encode('utf-8'))
    text_file.name = 'invalid.txt'

    response = client.post(
        "/question-answer",
        files={
            "question_file": ("questions.json", '[{"1": "Invalid file test."}]', "application/json"),
            "document_file": (text_file.name, text_file, "text/plain")
        }
    )

    # Validate the response for invalid file type
    assert response.status_code == 400
