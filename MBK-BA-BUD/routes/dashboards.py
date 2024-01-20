from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.budgets import Budget, BudgetBase
from models.budgets_categories import BudgetCategory, BudgetCategoryBase

from database import get_db
from models.budgets_history import BudgetHistory, BudgetHistoryBase
from models.dashboard import Dashboard

# Create a FastAPI router with a specific prefix and tags
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/{user_id}", response_model=Dashboard, status_code=status.HTTP_200_OK)
def get_dashboard_info(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Fetch budget information
    budget = db.query(Budget).filter(Budget.user_id == user_id).first()

    if not budget:
        # Raise an exception if the budget is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    # Fetch budget categories associated with the budget
    budgets_categories = db.query(BudgetCategory).filter(BudgetCategory.budget_id == budget.budget_id).all()

    # Fetch income and expense information from budget history
    incomes = (
        db.query(func.sum(BudgetHistory.amount))
        .filter(
            BudgetHistory.budgets_categories_id.in_([bc.budgets_categories_id for bc in budgets_categories]),
            BudgetHistory.type == True  # True indicates income in the BudgetHistory model
        )
        .scalar() or 0
    )

    expenses = (
        db.query(func.sum(BudgetHistory.amount))
        .filter(
            BudgetHistory.budgets_categories_id.in_([bc.budgets_categories_id for bc in budgets_categories]),
            BudgetHistory.type == False  # False indicates expense in the BudgetHistory model
        )
        .scalar() or 0
    )

    # Calculate remaining amount
    remaining_amount = budget.amount - expenses

    # Create and return the dashboard information
    dashboard_info = Dashboard(
        amount=budget.amount,
        remaining_amount=remaining_amount,
        income=incomes,
        expense=expenses
    )

    return dashboard_info
