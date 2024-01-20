# routes/users.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.budgets import Budget
from models.users import User, UserBase

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    # Create a new user record
    user_data = user.dict()
    user_data["created_at"] = datetime.now()
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # Retrieve a specific user by their ID
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    # Retrieve all users
    users = db.query(User).all()
    return users


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Delete a user by their ID
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    # Update an existing user by their ID
    user_data = user.dict()
    user_data["created_at"] = datetime.now()
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user.username = user_data["username"]
    db_user.email = user_data["email"]
    db_user.password_hash = user_data["password_hash"]
    db_user.first_name = user_data["first_name"]
    db_user.last_name = user_data["last_name"]
    db_user.date_of_birth = user_data["date_of_birth"]
    db_user.created_at = user_data["created_at"]
    db_user.profile_image = user_data["profile_image"]
    db.commit()
    return {"message": "User updated successfully"}


@router.get("/{user_id}/budget", status_code=status.HTTP_200_OK)
async def get_user_budget(user_id: int, db: Session = Depends(get_db)):
    # Retrieve the user with the specified user_id from the database
    user = db.query(User).filter(User.user_id == user_id).first()

    # Check if the user exists; raise an HTTPException if not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Retrieve the budget associated with the user from the database
    budget = db.query(Budget).filter(Budget.user_id == user.user_id).first()

    # Check if the budget exists; raise an HTTPException if not found
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found"
        )

    # Return the budget associated with the specified user_id
    return budget
