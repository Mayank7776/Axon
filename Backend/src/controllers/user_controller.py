from fastapi import APIRouter, Depends, Request, status, File, Form, UploadFile #type: ignore
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
async def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role_id: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    body = addUser(username=username, email=email, password=password, role_id=role_id)
    return add_user(body, image, db)

@router.put("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def update_user(
    request: Request,
    id: str,
    username: str | None = Form(None),
    email: str | None = Form(None),
    password: str | None = Form(None),
    role_id: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    body = updateUser(username=username, email=email, password=password, role_id=role_id)
    return update_user_by_id(id, body, image, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_user(request: Request , id: str, db: Session = Depends(get_db)):
    return delete_user_by_id(id, db)