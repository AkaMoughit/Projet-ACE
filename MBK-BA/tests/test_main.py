# tests/test_main.py
from fastapi.testclient import TestClient
import sys
import os

# Adding the project root directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 307  # Expecting a redirect (adjust based on your implementation)
    assert response.headers["location"] == "/docs"  # Adjust based on your implementation
