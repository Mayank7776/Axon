from src.utils.response import Response
from pydantic import BaseModel, Field #type: ignore
from typing import Optional

class addUser(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    username: str = Field(..., min_length=2, max_length=100)
    role_id: str = Field(...)
    
class updateUser(BaseModel):
    email: Optional[str] = Field(default=None, min_length=5, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    username: Optional[str] = Field(default=None, min_length=2, max_length=100)
    role_id: Optional[str] = Field(default=None)


# response schema 