from sqlalchemy import JSON, Column, Integer, String, ForeignKey, DateTime #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
from sqlalchemy.ext.mutable import MutableList #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class WorkoutDayExercise(Base):
    """
    Stores per-set breakdown for each exercise in a workout day.
 
    sets_data JSON structure:
    [
        { "set_number": 1,  target_reps:12 , "reps_performed": 8,  "weight_kg": 100.0, "rest_seconds": 90 },
        { "set_number": 2,  target_reps:12 , "reps_performed": 6,  "weight_kg": 105.0, "rest_seconds": 90 },
        { "set_number": 3,  target_reps:12 , "reps_performed": 6,  "weight_kg": 105.0, "rest_seconds": 120 },
        { "set_number": 4,  target_reps:12 , "reps_performed": 4,  "weight_kg": 110.0, "rest_seconds": 120 }
    ]
 
    Optional fields per set (all nullable so bodyweight / cardio work too):
        weight_kg    -- null for bodyweight exercises
        reps         -- null for time-based sets (use duration_seconds instead)
        duration_seconds -- e.g. plank holds, cardio intervals
        rest_seconds -- rest after this set; can vary per set
        notes        -- e.g. "drop set", "pause at bottom"
    """
 
    __tablename__ = "workout_day_exercises"
 
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    day_id = Column(String(36), ForeignKey("workout_days.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(String(36), ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    sets_data = Column(MutableList.as_mutable(JSON), nullable=False, default=list)
    # ^^^ list of set objects — see docstring above for shape
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
 
    # relationships
    day = relationship("WorkoutDay", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workout_day_exercises")
