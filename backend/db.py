import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Database file path ---
DB_PATH = os.path.join(os.path.dirname(__file__), "sheq.db")

# --- Engine and session ---
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# --- Base declarative class ---
Base = declarative_base()

# --- SQLAlchemy models ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_hash = Column(String(128), index=True, default="anonymous")
    channel = Column(String(32), default="web")
    text = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    flagged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer)
    reason = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Initialize DB and create tables if missing ---
def init_db():
    if not os.path.exists(DB_PATH):
        print(f"Creating new database at {DB_PATH}")
    Base.metadata.create_all(bind=engine)
