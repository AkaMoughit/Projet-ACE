# tests/test_users.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db, override_get_db
from main import app
from models.users import UserBase

# Constants
USER_ENDPOINT = "/users/1"
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

def test_create_user():
    # Test creating a user
    user_data = {
        "username": "test_user",
        "profile_image": "test_profile_image",
        "email": "test@example.com",
        "password_hash": "test_password",
        "first_name": "Test",
        "last_name": "User",
        "date_of_birth": "2000-01-01",
        "created_at": "2023-01-01T00:00:00",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_get_user():
    # Test getting a specific user
    response = client.get(USER_ENDPOINT)
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"

def test_get_users():
    # Test getting all users
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_user():
    # Test updating an existing user
    update_data = {
        "username": "updated_user",
        "email": "updated@example.com",
        "password_hash": "updated_password",
        "first_name": "Updated",
        "last_name": "User",
        "date_of_birth": "2000-01-01",
        "created_at": "2023-01-01T00:00:00",
        "profile_image": "updated_profile_image",
    }
    response = client.put(USER_ENDPOINT, json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"

def test_delete_user():
    # Test deleting a user
    response = client.delete(USER_ENDPOINT)
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_get_user_budget():
    # Test getting user's budget
    response = client.get(USER_ENDPOINT + "/budget")
    assert response.status_code == 404  # Assuming no budget is associated with the test user
    # You may adjust the assertion based on your actual logic
