# models/users.py
from datetime import datetime,date

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Text
from typing import Optional

from database import Base


class User(Base):
    # Database table name
    __tablename__ = "users"

    # Columns in the 'users' table
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    profile_image = Column(Text)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class UserBase(BaseModel):
    # Pydantic model for request input validation
    username: Optional[str]
    profile_image : Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    created_at: Optional[datetime]
