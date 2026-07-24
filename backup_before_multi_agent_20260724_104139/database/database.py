from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
	
DATABASE_URL = (
    "postgresql://postgres:root"
    "@localhost:5432/ai_healthcare_lab"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
Base = declarative_base()