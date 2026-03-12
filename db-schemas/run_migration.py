import os
from sqlalchemy import create_engine
from database import Base
from models import *  # This must be at module level to trigger all the declarative_base registrations

def run_migration():
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:////Users/vishalyadav/Documents/GP/gp_database.db"
    )
    
    print(f"Initializing database at: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print(f"✅ Created {len(Base.metadata.tables)} tables successfully!")

if __name__ == "__main__":
    run_migration()
