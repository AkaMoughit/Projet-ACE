# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from routes.budgets_history import router as budgets_history
from routes.budgets_categories import router as budgets_categories
from routes.dashboards import router as dashboard

# Create a FastAPI instance
app = FastAPI()

# Include user and budget routers
app.include_router(budgets_categories)
app.include_router(budgets_history)
app.include_router(dashboard)

# Create tables in the database
Base.metadata.create_all(bind=engine)


# Redirect the root URL to the documentation
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
