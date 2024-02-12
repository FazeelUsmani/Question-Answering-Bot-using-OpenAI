from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_question_answer():
    # Write tests for your endpoints
    # ...
