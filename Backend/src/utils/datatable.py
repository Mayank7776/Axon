from pydantic import BaseModel, Field #type: ignore
from typing import Optional


class DataTableFilter(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)

    search: Optional[str] = None

    sort_by: str = "created_at"
    sort_order: str = "desc"