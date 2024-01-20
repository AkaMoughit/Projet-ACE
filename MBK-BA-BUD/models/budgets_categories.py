from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, Boolean, DECIMAL, TIMESTAMP, ForeignKey, DateTime, Float
from database import Base

# Define the SQLAlchemy model for budget categories
class BudgetCategory(Base):
    __tablename__ = "budgets_categories"

    budgets_categories_id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer)  # ID of the associated budget
    budget_name = Column(String(255))  # Name of the budget category
    start_at = Column(DateTime)  # Start date of the budget category
    end_at = Column(DateTime)  # End date of the budget category
    amount = Column(Float)  # Total amount allocated for the budget category
    remaining_amount = Column(Float)  # Remaining amount for the budget category
    created_at = Column(DateTime)  # Timestamp indicating when the budget category was created
    updated_at = Column(DateTime)  # Timestamp indicating when the budget category was last updated
    deleted_at = Column(DateTime)  # Timestamp indicating when the budget category was deleted (soft delete)

# Define the Pydantic model for creating or updating budget categories
class BudgetCategoryBase(BaseModel):
    budgets_categories_id : int
    budget_id: int  # ID of the associated budget
    budget_name: str  # Name of the budget category
    start_at: date  # Start date of the budget category
    end_at: date  # End date of the budget category
    amount: float  # Total amount allocated for the budget category
    remaining_amount: float  # Remaining amount for the budget category
    created_at: datetime  # Timestamp for when the budget category was created
    updated_at: datetime  # Timestamp for when the budget category was last updated
    deleted_at: datetime  # Timestamp for when the budget category was deleted (soft delete)
