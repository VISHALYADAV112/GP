import os
from sqlalchemy import create_engine
from models import *  # Import all models at module level
from database import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:////Users/vishalyadav/Documents/GP/gp_database.db"
)

print(f"Initializing database at: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
print("✅ All 44+ tables created successfully!")
