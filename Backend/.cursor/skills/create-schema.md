# Skill: Create Schema

This skill outlines how to define request and response validation structures using Pydantic v2 in `src/schemas/`.

## Guidelines

1. **camelCase Request Schemas**:
   - Request structures for adding resources should start with `add` in camelCase (e.g., `addWorkoutPlan`, `addChatMessage`).
   - Request structures for updating resources should start with `update` in camelCase (e.g., `updateWorkoutPlan`, `updateChatMessage`).
2. **PascalCase Response Schemas**:
   - Outbound response payloads or sub-models should be named in PascalCase (e.g., `WorkoutPlanResponse`, `MessageDetail`).
3. Define strict constraints on fields (`Field(..., min_length=2, max_length=255)`) to enforce database size limits.
4. Import validation exceptions or helpers from Pydantic and typings (`Optional`, `List`).

## Example Schemas

```python
from pydantic import BaseModel, Field, EmailStr # type: ignore
from typing import Optional, List

class addExercise(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    muscle_group_id: str = Field(...)
    sets: int = Field(default=3, ge=1)
    reps: int = Field(default=10, ge=1)
    rest_seconds: Optional[int] = Field(default=60, ge=0)

class updateExercise(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    muscle_group_id: Optional[str] = Field(default=None)
    sets: Optional[int] = Field(default=None, ge=1)
    reps: Optional[int] = Field(default=None, ge=1)
    rest_seconds: Optional[int] = Field(default=None, ge=0)
```
