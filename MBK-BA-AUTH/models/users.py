# models/users.py
from datetime import datetime,date

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class User(Base):
    # Database table name
    __tablename__ = "users"

    # Columns in the 'users' table
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
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
    username: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    date_of_birth: date
    created_at: datetime
