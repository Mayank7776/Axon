from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
 
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
 
    # relationships
    user = relationship("User", back_populates="workout_plans")
    days = relationship(
        "WorkoutDay", back_populates="plan",
        cascade="all, delete-orphan",
        order_by="WorkoutDay.day_number"
    )