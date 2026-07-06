from fastapi import APIRouter, Depends, Request, status #type: ignore
from sqlalchemy.orm import Session #type: ignore
from src.core.db import get_db
from src.utils.rate_limiting import limiter
from src.modules.notifications.schemas import NotificationCreateSchema, MarkReadSchema
from src.modules.notifications.service import (
    create_notification_service,
    get_user_notifications_service,
    mark_as_read_service,
    mark_all_as_read_service,
    delete_notification_service
)

router = APIRouter()

@router.get("/")
@limiter.limit("50/minute")
async def get_notifications(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db)
):
    return get_user_notifications_service(user_id=user_id, db=db)

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_notification(
    request: Request,
    body: NotificationCreateSchema,
    db: Session = Depends(get_db)
):
    return create_notification_service(body=body, db=db)

@router.patch("/read-all")
@limiter.limit("20/minute")
async def mark_all_notifications_read(
    request: Request,
    body: MarkReadSchema,
    db: Session = Depends(get_db)
):
    return mark_all_as_read_service(user_id=body.user_id, db=db)

@router.patch("/{id}/read")
@limiter.limit("50/minute")
async def mark_notification_read(
    request: Request,
    id: str,
    body: MarkReadSchema,
    db: Session = Depends(get_db)
):
    return mark_as_read_service(notification_id=id, user_id=body.user_id, db=db)

@router.delete("/{id}")
@limiter.limit("20/minute")
async def delete_notification(
    request: Request,
    id: str,
    db: Session = Depends(get_db)
):
    return delete_notification_service(notification_id=id, db=db)
