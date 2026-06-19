# Skill: Create Controller

This skill shows how to construct clean controllers inside `src/controllers/` that adhere strictly to request/response handling.

## Guidelines

1. Always initialize `router = APIRouter()`.
2. Keep the controller method body extremely lean. It should only validate headers/body/params, call the service layer, and return the response.
3. Inject the DB session dependency using `db: Session = Depends(get_db)`.
4. Inject authentication when security is required: `current_user: User = Depends(validateToken)`.
5. Decorate all public and private routes with SlowAPI rate limiters: `@limiter.limit("rate/duration")`. This requires importing and passing `request: Request`.

## Template Code

```python
from fastapi import APIRouter, Depends, Request, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.rate_limiting import limiter
from src.controllers.dependency.auth_dependency import validateToken
from src.models.user_model import User
from src.schemas.my_schema import addMyEntity
from src.services.my_service import add_my_entity, delete_my_entity

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_entity(
    request: Request,
    body: addMyEntity,
    db: Session = Depends(get_db),
    current_user: User = Depends(validateToken)
):
    """
    Creates a new entity. Only authenticated users can perform this.
    """
    return add_my_entity(body, current_user.id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
def delete_entity(
    request: Request,
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(validateToken)
):
    """
    Deletes an entity. Verifies ownership in service layer.
    """
    return delete_my_entity(id, current_user, db)
```
