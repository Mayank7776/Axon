# Skill: Create CRUD Module (Modular Monolithic)

This skill outlines how to generate a complete new CRUD module in the backend, covering the structure inside `src/modules/<module_name>/`.

## Scaffolding Sequence

Follow this order when generating a new module:
1. **Create Directory**: Create `src/modules/<module_name>/`.
2. **Model (`models.py`)**: Define the database schema (SQLAlchemy).
3. **Schemas (`schemas.py`)**: Define the input and output Pydantic validations.
4. **Service (`service.py`)**: Implement database CRUD, pagination, filtering, and sorting.
5. **Router (`router.py`)**: Expose the endpoints, apply rate limiters (`@limiter.limit`), and inject dependencies.
6. **Register Route**: Register the router in `src/main.py`.
7. **Migrations**: Import the new model in `migrations/env.py` and generate the migration script.

---

## Detailed Example: `Category` Module

### 1. Database Model (`src/modules/categories/models.py`)
```python
from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime, timezone
import uuid
from src.core.db import Base

def utc_now():
    return datetime.now(timezone.utc)

class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
```

### 2. Pydantic Schemas (`src/modules/categories/schemas.py`)
```python
from pydantic import BaseModel, Field
from typing import Optional

class addCategory(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)

class updateCategory(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = Field(default=None)
```

### 3. Service Layer (`src/modules/categories/service.py`)
```python
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.modules.categories.models import Category
from src.modules.categories.schemas import addCategory, updateCategory
from src.utils.datatable import DataTableFilter
from src.utils.response import Response

def get_all_categories(filter: DataTableFilter, db: Session) -> Response:
    query = db.query(Category)
    
    if filter.search:
        search_pattern = f"%{filter.search}%"
        query = query.filter(
            or_(
                Category.name.ilike(search_pattern),
                Category.description.ilike(search_pattern)
            )
        )
        
    total_count = query.count()
    
    sort_column = getattr(Category, filter.sort_by, None)
    if sort_column is not None:
        if filter.sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(Category.created_at.desc())
        
    offset = (filter.page - 1) * filter.limit
    categories = query.offset(offset).limit(filter.limit).all()
    
    items = [{
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "is_active": c.is_active,
        "created_at": c.created_at
    } for c in categories]
    
    return Response(
        success=True,
        message="Categories list retrieved successfully",
        data={
            "items": items,
            "total": total_count,
            "page": filter.page,
            "limit": filter.limit
        }
    )

def add_category(body: addCategory, db: Session) -> Response:
    existing = db.query(Category).filter(Category.name == body.name).first()
    if existing:
        return Response(success=False, message="Category name already exists", data=None)
        
    new_cat = Category(name=body.name, description=body.description)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    
    return Response(success=True, message="Category created successfully", data={"id": new_cat.id})
```

### 4. Router Layer (`src/modules/categories/router.py`)
```python
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.datatable import DataTableFilter
from src.utils.rate_limiting import limiter
from src.modules.categories.schemas import addCategory
from src.modules.categories.service import get_all_categories, add_category

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def get_categories(request: Request, filter: DataTableFilter = Depends(), db: Session = Depends(get_db)):
    return get_all_categories(filter, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_category(request: Request, body: addCategory, db: Session = Depends(get_db)):
    return add_category(body, db)
```
