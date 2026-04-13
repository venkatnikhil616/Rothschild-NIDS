import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# DATABASE CONFIG

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = os.path.join(BASE_DIR, "database", "nids.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

# ENGINE

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite
    echo=False
)


# SESSION (THREAD-SAFE)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


# BASE CLASS FOR MODELS

Base = declarative_base()

# GET DB SESSION

def get_db():
    """
    Dependency-style DB session generator
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# INIT DATABASE

def init_db():
    """
    Create tables in DB
    """
    from database import models  # important: load models before create

    Base.metadata.create_all(bind=engine)
    print(" Database initialized successfully")


# CLOSE SESSION

def close_db():
    SessionLocal.remove()
