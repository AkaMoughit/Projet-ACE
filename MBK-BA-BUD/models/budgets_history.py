from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, Boolean, Float, TIMESTAMP, ForeignKey, DateTime
from database import Base
from typing import Optional

# Define the SQLAlchemy model for budget history
class BudgetHistory(Base):
    __tablename__ = "budgets_history"

    budgets_history_id = Column(Integer, primary_key=True, index=True)
    budgets_categories_id = Column(Integer)
    type = Column(Boolean)  # Assuming this column represents the type of budget history (True for income, False for expense)
    amount = Column(Float)
    created_at = Column(DateTime)  # Timestamp indicating when the budget history record was created
    updated_at = Column(DateTime)  # Timestamp indicating when the budget history record was last updated
    deleted_at = Column(DateTime)  # Timestamp indicating when the budget history record was deleted (soft delete)

# Define the Pydantic model for creating or updating budget history records
class BudgetHistoryBase(BaseModel):
    budgets_categories_id: int  # ID of the associated budget category
    type: bool  # Type of budget history (True for income, False for expense)
    amount: float  # Amount of the budget history record
    created_at: Optional[datetime]  # Optional timestamp for when the record was created
    updated_at: Optional[datetime]  # Optional timestamp for when the record was last updated
    deleted_at: Optional[datetime]  # Optional timestamp for when the record was deleted (soft delete)
