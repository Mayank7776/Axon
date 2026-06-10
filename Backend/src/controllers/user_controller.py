from fastapi import APIRouter, Depends, Request, status #type: ignore
from src.services.user_service import *
from sqlalchemy.orm import Session #type: ignore
from src.core.db import get_db
from src.utils.datatable import DataTableFilter
from src.utils.rate_limiting import limiter

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def get_users(request: Request , filter: DataTableFilter = Depends(), db: Session = Depends(get_db)):
    return get_all_users(filter, db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def get_user(request: Request , id: str, db: Session = Depends(get_db)):
    return get_user_by_id(id, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_user(request: Request , body: addUser, db: Session = Depends(get_db)):
    return add_user(body, db)

@router.put("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def update_user(request: Request , id: str, body: updateUser, db: Session = Depends(get_db)):
    return update_user_by_id(id, body, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_user(request: Request , id: str, db: Session = Depends(get_db)):
    return delete_user_by_id(id, db)