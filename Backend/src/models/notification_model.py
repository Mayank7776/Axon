from sqlalchemy import Column, String, Text, ForeignKey, DateTime #type: ignore
from sqlalchemy.orm import relationship #type: ignore
from datetime import datetime, timezone
from src.core.db import Base
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=True)
    redirect_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class UserNotificationRead(Base):
    __tablename__ = "user_notification_reads"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True)
    notification_id = Column(String(36), ForeignKey("notifications.id", ondelete="CASCADE"), primary_key=True, index=True)
    read_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User")
    notification = relationship("Notification")
