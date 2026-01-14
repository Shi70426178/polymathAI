from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/
DATABASE_URL = f"sqlite:///{BASE_DIR}/app/data/app.db"


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
