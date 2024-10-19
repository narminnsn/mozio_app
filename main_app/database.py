from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from main_app.config import settings  # Import settings

# Create database engine
POSTGRES_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@localhost/{settings.postgres_db}"
engine = create_engine(POSTGRES_DATABASE_URL)  # Database engine creation

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()
