from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.users import User, UserBase

# Create a FastAPI router with a specific prefix and tags
router = APIRouter(prefix="/login", tags=["Login"])

# Endpoint to handle user login
@router.post("/", status_code=status.HTTP_200_OK)
async def login_user(user_email: str, user_password: str, db: Session = Depends(get_db)):
    # Query the database for a user with the provided email and password
    user = db.query(User).filter(User.email == user_email, User.password_hash == user_password).first()
    
    # If the user is not found, raise an HTTP exception
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Return the user_id if the login is successful
    return user.user_id
