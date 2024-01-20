from datetime import datetime, date

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Float

from database import Base

class Dashboard(BaseModel) :
    # Pydantic model for request input validation
    amount: int = 0  # Default value for the total amount allocated for the budget
    remaining_amount: int = 0  # Default value for the remaining amount for the budget
    income: int = 0
    expense: int = 0
