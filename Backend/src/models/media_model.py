from sqlalchemy import Boolean, Column, Enum, Integer, String, ForeignKey, DateTime #type: ignore
from datetime import datetime, timezone #type: ignore
from src.core.db import Base
from sqlalchemy.orm import relationship #type: ignore
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class ExerciseMedia(Base):
    __tablename__ = "exercise_media"
 
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exercise_id = Column(String(36), ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    media_type = Column(
        Enum("image", "video", name="media_type_enum"),
        nullable=False
    )
    provider = Column(
        Enum("azure", "aws", name="storage_provider_enum"),
        nullable=False
    )
    storage_key = Column(String(1000), nullable=False)   # raw blob path e.g. exercises/bench-press/demo.mp4
    cdn_url = Column(String(1000), nullable=False)        # public-facing CDN / signed URL
    mime_type = Column(String(100), nullable=True)        # e.g. image/jpeg, video/mp4
    file_size_kb = Column(Integer, nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), default=utc_now)
 
    # relationships
    exercise = relationship("Exercise", back_populates="media")