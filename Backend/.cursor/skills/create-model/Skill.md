# Skill: Create Model

This skill outlines how to build SQLAlchemy database models inside `src/models/` and link them to the project database schema.

## Guidelines

1. Inherit all models from the base class: `from src.core.db import Base`.
2. Map tables to pluralized, snake_case strings: `__tablename__ = "table_names"`.
3. Use a 36-character UUID string as the primary key by default:
   ```python
   id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
   ```
4. Define relationships clearly. Always use `back_populates` on both sides of the relationship rather than `backref`.
5. Enforce cascading deletes explicitly on parent-child relations if the child depends fully on the parent: `cascade="all, delete-orphan"`.
6. Always register models by importing them inside `src/models/__init__.py` to ensure Alembic autogenerate captures them.

## Example Model File

```python
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from datetime import datetime, timezone
import uuid
from src.core.db import Base

def utc_now():
    return datetime.now(timezone.utc)

class WorkoutDay(Base):
    __tablename__ = "workout_days"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)
    name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    plan = relationship("WorkoutPlan", back_populates="days")
```
