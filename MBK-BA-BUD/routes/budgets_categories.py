from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.budgets import Budget, BudgetBase

from database import get_db
from models.budgets_categories import BudgetCategory, BudgetCategoryBase

# Create an APIRouter instance with a specific prefix and tags
router = APIRouter(prefix="/budgets/categories", tags=["Budgets_Categories"])

# Endpoint to create budget categories
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_budgets_categories(budgets_categories: BudgetCategoryBase, db: Session = Depends(get_db)):
    # Retrieve the associated budget from the database
    budget = db.query(Budget).filter(Budget.budget_id == budgets_categories.budget_id).first()
    
    # Check if the budget exists, raise an exception if not found
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found"
        )
    
    # Check if the budget has enough remaining amount for the new category, raise an exception if not enough
    if budget.remaining_amount < budgets_categories.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Budget not enough"
        )
    
    # Prepare data for creating a new budget category
    budgets_categories_data = budgets_categories.dict()
    budgets_categories_data["created_at"] = datetime.now()
    budgets_categories_data["remaining_amount"] = budgets_categories_data["amount"]
    
    # Create a new budget category in the database
    db_budgets_categories = BudgetCategory(**budgets_categories_data)
    db.add(db_budgets_categories)
    db.commit()
    
    # Update the remaining amount in the associated budget
    budget.remaining_amount = budget.remaining_amount - db_budgets_categories.amount
    db.commit()
    
    return {"message": "Budgets_Categories created successfully"}

# Endpoint to retrieve all budget categories
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_budgets_categories(db: Session = Depends(get_db)):
    # Retrieve all budget categories from the database
    budgets_categories = db.query(BudgetCategory).all()
    return budgets_categories

# Endpoint to retrieve a specific budget category by ID
@router.get("/{budgets_categories_id}", status_code=status.HTTP_200_OK)
async def get_budgets_categories_by_id(budgets_categories_id: int, db: Session = Depends(get_db)):
    # Retrieve a specific budget category by ID from the database
    budgets_categories = db.query(BudgetCategory).filter(BudgetCategory.budgets_categories_id == budgets_categories_id).first()

    # Check if the budget category exists, raise an exception if not found
    if not budgets_categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budgets_Categories with id {budgets_categories_id} not found")

    return budgets_categories

# Endpoint to update a specific budget category by ID
@router.put("/{budgets_categories_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_budgets_categories(budgets_categories_id: int, budgets_categories: BudgetCategoryBase, db: Session = Depends(get_db)):
    # Extract data from the request and set the update timestamp
    budgets_categories_data = budgets_categories.dict()
    budgets_categories_data["updated_at"] = datetime.now()

    # Update the specified budget category in the database
    db.query(BudgetCategory).filter(BudgetCategory.budgets_categories_id == budgets_categories_id).update(budgets_categories_data)
    db.commit()

    return {"message": "Budgets_Categories updated successfully"}

# Endpoint to delete a specific budget category by ID
@router.delete("/{budgets_categories_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_budgets_categories(budgets_categories_id: int, db: Session = Depends(get_db)):
    # Delete the specified budget category from the database
    db.query(BudgetCategory).filter(BudgetCategory.budgets_categories_id == budgets_categories_id).delete(synchronize_session=False)
    db.commit()

    return {"message": "Budgets_Categories deleted successfully"}

# Endpoint to retrieve all budget categories associated with a specific budget ID
@router.get("/budget/{budget_id}", status_code=status.HTTP_200_OK)
async def get_budgets_categories_by_budget_id(budget_id: int, db: Session = Depends(get_db)):
    # Retrieve all budget categories associated with the specified budget ID from the database
    budgets_categories = db.query(BudgetCategory).filter(BudgetCategory.budget_id == budget_id).all()

    # Check if any budget categories are associated with the specified budget ID, raise an exception if not found
    if not budgets_categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budgets_Categories with budget_id {budget_id} not found")

    return budgets_categories

# Endpoint to retrieve all budget categories associated with a specific user ID
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_budgets_categories_by_user_id(user_id: int, db: Session = Depends(get_db)):
    # Retrieve the user's budget and all associated budget categories
    budget = db.query(Budget).filter(Budget.user_id == user_id).first()
    budgets_categories = db.query(BudgetCategory).filter(BudgetCategory.budget_id == budget.budget_id).all()

    # Check if any budget categories are associated with the specified user ID, raise an exception if not found
    if not budgets_categories or not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budgets_Categories with user_id {user_id} not found")

    return budgets_categories