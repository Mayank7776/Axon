# Skill: Create Router

This skill shows how to construct routers inside `src/modules/<module_name>/router.py` that handle request/response orchestration.

## Guidelines

1. Initialize `router = APIRouter()`.
2. Keep the router method body lean: validate headers/body/params, call the service layer, and return the response wrapper.
3. Inject the DB session: `db: Session = Depends(get_db)`.
4. Inject authentication when security is required: `current_user: User = Depends(validateToken)` from `src.modules.auth.dependency`.
5. Decorate all public and private routes with SlowAPI rate limiters: `@limiter.limit("rate/duration")`. This requires importing and passing `request: Request`.

## Template Code

```python
# src/modules/items/router.py
from fastapi import APIRouter, Depends, Request, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.rate_limiting import limiter
from src.modules.auth.dependency import validateToken
from src.modules.users.models import User
from src.modules.items.schemas import addMyEntity
from src.modules.items.service import add_my_entity, delete_my_entity

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_entity(
    request: Request,
    body: addMyEntity,
    db: Session = Depends(get_db),
    current_user: User = Depends(validateToken)
):
    return add_my_entity(body, current_user.id, db)
```
