from sqlalchemy import Column, Integer, String, ForeignKey, DateTime #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class WorkoutDay(Base):
    __tablename__ = "workout_days"
 
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    label = Column(String(100), nullable=True)   # e.g. "Push Day", "Leg Day", "Rest"
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
 
    # relationships
    plan = relationship("WorkoutPlan", back_populates="days")
    exercises = relationship("WorkoutDayExercise", back_populates="day", cascade="all, delete-orphan", order_by="WorkoutDayExercise.sort_order")
 