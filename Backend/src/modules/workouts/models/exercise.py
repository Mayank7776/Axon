from sqlalchemy import Boolean, Column, Enum, String, ForeignKey, DateTime, Text #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class Exercise(Base):
    __tablename__ = "exercises"
 
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    muscle_group_id = Column(String(36), ForeignKey("muscle_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(
        Enum("machine", "free_weights", "compound", "bodyweight", name="exercise_category_enum"),
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
 
    # relationships
    muscle_group = relationship("MuscleGroup", back_populates="exercises")
    created_by_user = relationship("User", back_populates="exercises_created", foreign_keys=[created_by])
    media = relationship(
        "Media",
        primaryjoin="and_(Exercise.id==foreign(Media.entity_id), Media.entity_type=='exercise')",
        cascade="all, delete-orphan",
        order_by="Media.sort_order"
    )
    workout_day_exercises = relationship("WorkoutDayExercise", back_populates="exercise")
