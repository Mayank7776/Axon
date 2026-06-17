from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, JSON, Date #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class UserWorkoutStats(Base):
    """
    Stores workout stats logged by a user for a workout day.

    exercises_data JSON structure:
    [
        {
            "exercise_id": "uuid-string-of-exercise",
            "exercise_name": "Bench Press",
            "sort_order": 1,
            "sets": [
                {
                    "set_number": 1,
                    "target_reps": 12,
                    "reps_performed": 10,
                    "weight_kg": 60.0,
                    "rest_seconds": 90,
                    "is_completed": true
                },
                {
                    "set_number": 2,
                    "target_reps": 12,
                    "reps_performed": 8,
                    "weight_kg": 65.0,
                    "rest_seconds": 90,
                    "is_completed": false
                }
            ]
        }
    ]
    """
    __tablename__ = "user_workout_stats"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    workout_plan_id = Column(String(36), ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)
    day_label = Column(String(100), nullable=True)
    workout_date = Column(Date, nullable=False, index=True)
    exercises_data = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=utc_now, nullable=True)

    # relationships
    user = relationship("User")
    workout_plan = relationship("WorkoutPlan")
