from pydantic import BaseModel, Field #type: ignore
from typing import List, Optional

class ExerciseSet(BaseModel):
    set_number: int = Field(..., ge=1)
    target_reps: int = Field(..., ge=1)
    reps_performed: Optional[int] = None
    weight_kg: Optional[float] = None
    rest_seconds: Optional[int] = None

class WorkoutDayExerciseItem(BaseModel):
    exercise_id: str = Field(...)
    sort_order: int = Field(..., ge=0)
    sets: List[ExerciseSet] = Field(...)

class WorkoutDayItem(BaseModel):
    day_number: int = Field(..., ge=1, le=7)
    exercises: List[WorkoutDayExerciseItem] = Field(...)

class UpsertWorkoutPlan(BaseModel):
    id: Optional[str] = None
    user_id: str = Field(...)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    is_active: Optional[bool] = False
    days: List[WorkoutDayItem] = Field(...)

class UpsertWorkoutPlanMetadata(BaseModel):
    id: Optional[str] = None
    user_id: str = Field(...)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    is_active: Optional[bool] = False

class UpsertWorkoutDay(BaseModel):
    id: Optional[str] = None
    plan_id: str = Field(...)
    day_number: int = Field(..., ge=1, le=7)
    exercises: List[WorkoutDayExerciseItem] = Field(...)

class AISetItem(BaseModel):
    set_number: int = Field(..., ge=1)
    target_reps: int = Field(..., ge=1)
    reps_performed: Optional[int] = None
    weight_kg: Optional[float] = None
    rest_seconds: Optional[int] = None

class AIExerciseItem(BaseModel):
    exercise_name: str = Field(...)
    sort_order: int = Field(..., ge=0)
    sets: List[AISetItem] = Field(...)

class AIDayItem(BaseModel):
    day_number: int = Field(..., ge=1, le=7)
    exercises: List[AIExerciseItem] = Field(...)

class SaveAIWorkoutPlanPayload(BaseModel):
    user_id: str = Field(...)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    days: List[AIDayItem] = Field(...)

class WorkoutStatsSetItem(BaseModel):
    set_number: int = Field(..., ge=1)
    target_reps: int = Field(..., ge=1)
    reps_performed: Optional[int] = None
    weight_kg: Optional[float] = None
    rest_seconds: Optional[int] = None
    is_completed: bool = Field(default=False)

class WorkoutStatsExerciseItem(BaseModel):
    exercise_id: str = Field(...)
    exercise_name: str = Field(...)
    sort_order: int = Field(..., ge=0)
    sets: List[WorkoutStatsSetItem] = Field(...)

class SaveUserWorkoutStatsPayload(BaseModel):
    user_id: str = Field(...)
    workout_plan_id: str = Field(...)
    day_number: int = Field(..., ge=1, le=7)
    day_label: Optional[str] = None
    workout_date: Optional[str] = None
    exercises_data: List[WorkoutStatsExerciseItem] = Field(...)

