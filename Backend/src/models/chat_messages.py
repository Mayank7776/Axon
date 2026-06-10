from sqlalchemy import Column, Enum, String, ForeignKey, DateTime, Text #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
 
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(
        Enum("user", "assistant", name="message_role_enum"),
        nullable=False
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
 
    # relationships
    session = relationship("ChatSession", back_populates="messages")