import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# ---------------------------
# DATABASE CONFIG
# ---------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)  # ✅ ensure folder exists

DB_PATH = os.path.join(DB_DIR, "nids.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"


# ---------------------------
# ENGINE
# ---------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite + threads
    pool_pre_ping=True,  # ✅ avoids stale connections
    echo=False
)


# ---------------------------
# SESSION (THREAD SAFE)
# ---------------------------
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)


# ---------------------------
# BASE CLASS
# ---------------------------
Base = declarative_base()


# ---------------------------
# GET DB SESSION
# ---------------------------
def get_db():
    """
    Dependency-style DB session generator
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# INIT DATABASE
# ---------------------------
def init_db():
    """
    Create tables safely
    """
    try:
        from database import models  # 🔥 ensures models are loaded

        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")

    except Exception as e:
        print(f"❌ DB Init Error: {e}")
        raise


# ---------------------------
# CLOSE SESSION
# ---------------------------
def close_db():
    """
    Remove scoped session (important for threads)
    """
    SessionLocal.remove()
