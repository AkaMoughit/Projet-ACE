# routes/budgets.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.budgets import Budget, BudgetBase

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_budget(budget: BudgetBase, db: Session = Depends(get_db)):
    # Create a new budget record
    budget_data = budget.dict()
    budget_data["created_at"] = datetime.now()
    budget_data["remaining_amount"] = budget_data["amount"]
    db_budget = Budget(**budget_data)
    db.add(db_budget)
    db.commit()
    return {"message": "Budget created successfully"}


@router.get("/{budget_id}", status_code=status.HTTP_200_OK)
async def get_budget(budget_id: int, db: Session = Depends(get_db)):
    # Retrieve a specific budget by its ID
    budget = db.query(Budget).filter(Budget.budget_id == budget_id).first()
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found"
        )
    return budget


@router.get("/", status_code=status.HTTP_200_OK)
async def get_budgets(db: Session = Depends(get_db)):
    # Retrieve all budgets
    budgets = db.query(Budget).all()


    return budgets


@router.delete("/{budget_id}", status_code=status.HTTP_200_OK)
async def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    # Delete a budget by its ID
    budget = db.query(Budget).filter(Budget.budget_id == budget_id).first()
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found"
        )
    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}


@router.put("/{budget_id}", status_code=status.HTTP_200_OK)
async def update_budget(
    budget_id: int, budget: BudgetBase, db: Session = Depends(get_db)
):
    # Update an existing budget by its ID
    budget_data = budget.dict()
    budget_data["created_at"] = datetime.now()
    db_budget = db.query(Budget).filter(Budget.budget_id == budget_id).first()
    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found"
        )
    db_budget.user_id = budget_data["user_id"]
    db_budget.budget_name = budget_data["budget_name"]
    db_budget.amount = budget_data["amount"]
    db_budget.remaining_amount = budget_data["amount"]
    db_budget.start_at = budget_data["start_at"]
    db_budget.end_at = budget_data["end_at"]
    db_budget.created_at = budget_data["created_at"]
    db.commit()
    return {"message": "Budget updated successfully"}

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_budgets_by_user(user_id: int, db: Session = Depends(get_db)):
    # Retrieve all budgets
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    return budgets
