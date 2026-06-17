from fastapi import HTTPException #type: ignore
from sqlalchemy.orm import Session #type: ignore
from src.models.notification_model import Notification, UserNotificationRead
from src.models.user_model import User
from src.schemas.notification_schema import NotificationCreateSchema

def create_notification_service(body: NotificationCreateSchema, db: Session):
    notification = Notification(
        title=body.title,
        message=body.message,
        type=body.type,
        redirect_url=body.redirect_url
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_user_notifications_service(user_id: str, db: Session):
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all global notifications
    notifications = db.query(Notification).order_by(Notification.created_at.desc()).all()

    # Fetch read notifications for this user
    read_records = db.query(UserNotificationRead).filter(UserNotificationRead.user_id == user_id).all()
    read_ids = {r.notification_id for r in read_records}

    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "redirect_url": n.redirect_url,
            "created_at": n.created_at,
            "is_read": n.id in read_ids
        })
    return result

def mark_as_read_service(notification_id: str, user_id: str, db: Session):
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate notification exists
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    # Check if already read
    existing = db.query(UserNotificationRead).filter(
        UserNotificationRead.user_id == user_id,
        UserNotificationRead.notification_id == notification_id
    ).first()

    if not existing:
        read_record = UserNotificationRead(user_id=user_id, notification_id=notification_id)
        db.add(read_record)
        db.commit()

    return {"message": "Notification marked as read"}

def mark_all_as_read_service(user_id: str, db: Session):
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all global notifications
    notifications = db.query(Notification).all()
    all_notification_ids = {n.id for n in notifications}

    # Fetch already read records
    read_records = db.query(UserNotificationRead).filter(UserNotificationRead.user_id == user_id).all()
    read_ids = {r.notification_id for r in read_records}

    # Identify unread IDs
    unread_ids = all_notification_ids - read_ids

    # Bulk insert read records
    for notif_id in unread_ids:
        db.add(UserNotificationRead(user_id=user_id, notification_id=notif_id))

    if unread_ids:
        db.commit()

    return {"message": "All notifications marked as read"}

def delete_notification_service(notification_id: str, db: Session):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notif)
    db.commit()
    return {"message": "Notification deleted successfully"}
