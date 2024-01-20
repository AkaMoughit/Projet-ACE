# database.py
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables with defaults
DB_USER = os.getenv("DB_USER", "doadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "AVNS_bM9-yo76Q3fg1XgP1w2")
DB_HOST = os.getenv("DB_HOST", "mbk-db-do-user-14057762-0.c.db.ondigitalocean.com")
DB_PORT = os.getenv("DB_PORT", "25060")
DB_NAME = os.getenv("DB_NAME", "defaultdb")

# Use an f-string to construct the database URL for better readability
URL_DATABASE = (
    f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl-mode="
)

# Use the create_engine function with additional parameters
# to enable more secure connection settings
engine = create_engine(
    URL_DATABASE,
    pool_pre_ping=True,  # Enable connection pool pre-ping to check the database connection health
    echo=False,  # Set to True if you want to see SQL queries in the console
)

# Create a SessionLocal class using sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base
Base = declarative_base()


# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
