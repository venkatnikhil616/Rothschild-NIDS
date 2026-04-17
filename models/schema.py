# ---------------------------
# IMPORTS
# ---------------------------
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from flask_login import UserMixin
from database.db import Base


# ---------------------------
# LOG MODEL
# ---------------------------
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    protocol_type = Column(String, nullable=True)
    service = Column(String, nullable=True)
    flag = Column(String, nullable=True)

    src_bytes = Column(Integer, default=0)
    dst_bytes = Column(Integer, default=0)

    attack_type = Column(String, default="normal")
    confidence = Column(Float, default=0.0)
    severity = Column(String, default="low")

    event_type = Column(String, default="network")

    timestamp = Column(DateTime, default=datetime.utcnow)


# ---------------------------
# ALERT MODEL
# ---------------------------
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    attack_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)


# ---------------------------
# USER MODEL
# ---------------------------
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    # Flask-Login requirement
    def get_id(self):
        return str(self.id)
