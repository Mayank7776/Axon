from typing import Optional
from fastapi import UploadFile #type: ignore
from pydantic import BaseModel, ConfigDict


class UpsertMuscleGroup(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

class upsertExcercise(BaseModel):
    id: Optional[str] = None
    muscle_group_id: str
    created_by: Optional[str] = None
    name: str
    description: Optional[str] = None
    category: str