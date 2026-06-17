from pydantic import BaseModel, Field #type: ignore
from typing import Optional
from datetime import datetime

class NotificationCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    type: Optional[str] = Field(None, max_length=50)
    redirect_url: Optional[str] = Field(None, max_length=500)

class MarkReadSchema(BaseModel):
    user_id: str

class NotificationResponseSchema(BaseModel):
    id: str
    title: str
    message: str
    type: Optional[str]
    redirect_url: Optional[str]
    created_at: datetime
    is_read: bool
