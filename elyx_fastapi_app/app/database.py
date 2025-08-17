from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path

# Import Base from models
from app.models.database import Base

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./elyx_journey.db")

# Create database directory if it doesn't exist
db_path = Path("./elyx_journey.db")
db_path.parent.mkdir(exist_ok=True)

# Engine configuration
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Set to True for SQL query logging
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=False
    )

# Session configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Drop all tables (for development/testing)
def drop_tables():
    Base.metadata.drop_all(bind=engine)
