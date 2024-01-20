from datetime import datetime, date

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Float

from database import Base

# Define the SQLAlchemy model for budget records
class Budget(Base):
    # Database table name
    __tablename__ = "budgets"

    # Columns in the 'budgets' table
    budget_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  # ID of the user associated with the budget
    budget_name = Column(String(255))  # Name of the budget
    amount = Column(Float)  # Total amount allocated for the budget
    remaining_amount = Column(Float)  # Remaining amount for the budget
    start_at = Column(DateTime)  # Start date of the budget
    end_at = Column(DateTime)  # End date of the budget
    created_at = Column(DateTime)  # Timestamp indicating when the budget was created
    updated_at = Column(DateTime)  # Timestamp indicating when the budget was last updated
    deleted_at = Column(DateTime)  # Timestamp indicating when the budget was deleted (soft delete)

# Define the Pydantic model for creating or updating budget records
class BudgetBase(BaseModel):
    # Pydantic model for request input validation
    user_id: int  # ID of the user associated with the budget
    budget_name: str  # Name of the budget
    amount: int = 0  # Default value for the total amount allocated for the budget
    remaining_amount: int = 0  # Default value for the remaining amount for the budget
    start_at: date  # Start date of the budget
    end_at: date  # End date of the budget
    created_at: datetime  # Timestamp for when the budget was created
