from pydantic import BaseModel #type: ignore
from typing import Optional

class BlogCategoryResponse(BaseModel):
    id: str
    name: str
    slug: str

class BlogUpsertSchema(BaseModel):
    id: Optional[str] = None
    created_by: str
    title: str
    content: str
    category_id: str
    excerpt: Optional[str] = None
    is_published: bool = False
