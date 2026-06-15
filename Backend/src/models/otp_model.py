from sqlalchemy import Column, String, DateTime, ForeignKey #type: ignore
from sqlalchemy.orm import relationship #type: ignore
from datetime import datetime, timezone, timedelta
import uuid

from src.core.db import Base

def utc_now():
    return datetime.now(timezone.utc)

class LoginOtp(Base):
    __tablename__ = "login_otps"

    id = Column(String(36),primary_key=True,default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36),ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    otp = Column(String(6),nullable=False)
    expires_at = Column(DateTime(timezone=True),nullable=False)
    user = relationship("User")