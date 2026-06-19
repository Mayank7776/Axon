# Skill: Create CRUD Module

This skill outlines the process of generating a complete new CRUD module in the FastAPI backend, covering the Model, Schemas, Service, Controller, and Database Migration.

## Scaffolding Sequence

Follow this order when generating a new module:
1. **Model**: Create the SQLAlchemy model inside `src/models/` and export it in `src/models/__init__.py`.
2. **Schemas**: Create the input and output Pydantic schemas in `src/schemas/`.
3. **Service**: Implement CRUD, filtering, searching, sorting, and pagination logic in `src/services/`.
4. **Controller**: Define HTTP endpoints, rate-limits, validation, and invoke services in `src/controllers/`.
5. **Register Routes**: Add the controller router to `src/main.py`.
6. **Migration**: Generate Alembic migration file.

---

## Detailed Example: `Category` Module

### 1. Database Model (`src/models/category.py`)
```python
from sqlalchemy import Column, String, DateTime, Boolean # type: ignore
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

### 2. Pydantic Schemas (`src/schemas/category_schema.py`)
```python
from pydantic import BaseModel, Field # type: ignore
from typing import Optional

class addCategory(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)

class updateCategory(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = Field(default=None)
```

### 3. Service Layer (`src/services/category_service.py`)
```python
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.category import Category
from src.schemas.category_schema import addCategory, updateCategory
from src.utils.datatable import DataTableFilter
from src.utils.response import Response

def get_all_categories(filter: DataTableFilter, db: Session) -> Response:
    query = db.query(Category)
    
    # Search
    if filter.search:
        search_pattern = f"%{filter.search}%"
        query = query.filter(
            or_(
                Category.name.ilike(search_pattern),
                Category.description.ilike(search_pattern)
            )
        )
        
    total_count = query.count()
    
    # Sorting
    sort_column = getattr(Category, filter.sort_by, None)
    if sort_column is not None:
        if filter.sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(Category.created_at.desc())
        
    # Pagination
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

### 4. Controller Layer (`src/controllers/category_controller.py`)
```python
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.datatable import DataTableFilter
from src.utils.rate_limiting import limiter
from src.schemas.category_schema import addCategory
from src.services.category_service import get_all_categories, add_category

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
