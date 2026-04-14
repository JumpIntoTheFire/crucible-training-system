import os
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/cts_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# -------------------------
# Contact Model
# -------------------------
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


# -------------------------
# Exercise Model
# -------------------------
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    force = Column(String)
    level = Column(String)
    mechanic = Column(String)
    equipment = Column(String)
    primaryMuscles = Column(ARRAY(String))
    secondaryMuscles = Column(ARRAY(String))
    instructions = Column(ARRAY(Text))
    category = Column(String)
    startImage = Column(Text)
    endImage = Column(Text)


# -------------------------
# User Model
# -------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    workout_plans = relationship("WorkoutPlan", back_populates="owner", cascade="all, delete-orphan")


# -------------------------
# WorkoutPlan Model
# -------------------------
class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    exercises = Column(JSONB, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="workout_plans")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
