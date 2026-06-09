from sqlalchemy import create_engine #type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base #type: ignore
from src.core.settings import settings

Base = declarative_base()
engine = create_engine(settings.DB_CONNECTION)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
