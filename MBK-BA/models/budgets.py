# models/budgets.py
from datetime import datetime,date

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Float
from typing import Optional

from database import Base


class Budget(Base):
    # Database table name
    __tablename__ = "budgets"

    # Columns in the 'budgets' table
    budget_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    budget_name = Column(String(255))
    amount = Column(Float)
    remaining_amount = Column(Float)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class BudgetBase(BaseModel):
    # Pydantic model for request input validation
    user_id: Optional[int]
    budget_name: Optional[str]
    amount: Optional[int] = 0
    remaining_amount: Optional[int] = 0
    start_at: Optional[date]
    end_at: Optional[date]
    created_at: Optional[datetime]
