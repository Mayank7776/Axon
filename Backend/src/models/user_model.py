from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    # relationship
    role = relationship("Role", back_populates="users")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    exercises_created = relationship("Exercise", back_populates="created_by_user", foreign_keys="Exercise.created_by")
    workout_plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")    
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    nutrition_charts = relationship("NutritionChart", back_populates="creator", cascade="all, delete-orphan")