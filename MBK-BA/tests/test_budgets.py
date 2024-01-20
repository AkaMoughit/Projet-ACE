# tests/test_budgets.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db, override_get_db
from main import app
from models.budgets import BudgetBase

# Constants
BUDGET_ENDPOINT = "/budgets/1"
DATABASE_URL = "sqlite:///:memory:"

# Override database URL in the test settings
app.dependency_overrides[get_db] = override_get_db

# Create a testing session and apply the overrides
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app.dependency_overrides[get_db] = override_get_db

# Create tables in the in-memory database
Base.metadata.create_all(bind=engine)

# Create a test client
client = TestClient(app)

def test_create_budget():
    # Test creating a budget
    budget_data = {
        "user_id": 1,
        "budget_name": "Test Budget",
        "amount": 1000,
        "remaining_amount": 1000,
        "start_at": "2023-01-01",
        "end_at": "2023-12-31",
        "created_at": "2023-01-01T00:00:00",
    }
    response = client.post("/budgets/", json=budget_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Budget created successfully"

def test_get_budget():
    # Test getting a specific budget
    response = client.get(BUDGET_ENDPOINT)
    assert response.status_code == 200
    assert response.json()["user_id"] == 1

def test_get_budgets():
    # Test getting all budgets
    response = client.get("/budgets/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_budget():
    # Test updating an existing budget
    update_data = {
        "user_id": 1,
        "budget_name": "Updated Budget",
        "amount": 1500,
        "remaining_amount": 1500,
        "start_at": "2023-01-01",
        "end_at": "2023-12-31",
        "created_at": "2023-01-01T00:00:00",
    }
    response = client.put(BUDGET_ENDPOINT, json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Budget updated successfully"

def test_delete_budget():
    # Test deleting a budget
    response = client.delete(BUDGET_ENDPOINT)
    assert response.status_code == 200
    assert response.json()["message"] == "Budget deleted successfully"

def test_get_budgets_by_user():
    # Test getting budgets by user
    response = client.get(BUDGET_ENDPOINT)
    assert response.status_code == 200
    assert len(response.json()) > 0
