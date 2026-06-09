from pydantic import BaseModel, Field #type: ignore
from typing import Optional

class addRole(BaseModel):
    # "..." means required field
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
    
class updateRole(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
