from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean #type:ignore
from sqlalchemy.orm import relationship #type:ignore
from datetime import datetime, timezone
import uuid

from src.core.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    token = Column(
        String(500),
        nullable=False,
        unique=True
    )

    is_revoked = Column(
        Boolean,
        default=False
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now
    )

    user = relationship(
        "User",
        back_populates="refresh_tokens"
    )