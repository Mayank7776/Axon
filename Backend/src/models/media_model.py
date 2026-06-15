from sqlalchemy import ( #type: ignore
    Boolean,
    Column,
    Enum,
    Integer,
    String,
    DateTime,
)
from datetime import datetime, timezone
from src.core.db import Base
import uuid


def utc_now():
    return datetime.now(timezone.utc)


class Media(Base):
    __tablename__ = "media"

    id = Column(String(36),primary_key=True,default=lambda: str(uuid.uuid4()))
    # Entity reference
    entity_type = Column(Enum("exercise", "blog", "diet_chart", "workout_plan", "user_profile", name="entity_type_enum"),nullable=False,index=True)
    entity_id = Column(String(36),nullable=False,index=True)
    media_type = Column(Enum("image", "video", name="media_type_enum"),nullable=False)
    provider = Column(Enum( "cloudinary", "azure", "aws", name="storage_provider_enum"),nullable=False)
    storage_key = Column(String(1000),nullable=False)
    cdn_url = Column(String(1000),nullable=False)
    mime_type = Column(String(100),nullable=True)
    file_size_kb = Column(Integer,nullable=True)
    public_id = Column(String(500),nullable=True)
    is_primary = Column(Boolean,default=False,nullable=False)
    sort_order = Column(Integer,default=0,nullable=False)
    uploaded_at = Column(DateTime(timezone=True),default=utc_now)