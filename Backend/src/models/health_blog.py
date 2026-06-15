from sqlalchemy import ( #type:ignore
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship #type:ignore
from datetime import datetime, timezone
from src.core.db import Base
import uuid

def utc_now():
    return datetime.now(timezone.utc)

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(String(36),primary_key=True,default=lambda: str(uuid.uuid4()))
    created_by = Column(String(36),ForeignKey("users.id"),nullable=False,index=True)
    title = Column(String(255),nullable=False)
    slug = Column(String(255),unique=True,nullable=False,index=True)
    excerpt = Column(String(500),nullable=True)
    content = Column(Text,nullable=False)
    category = Column(String(100),nullable=True)
    is_published = Column(Boolean,default=False,nullable=False)
    created_at = Column(DateTime(timezone=True),default=utc_now)
    updated_at = Column(DateTime(timezone=True),default=utc_now,onupdate=utc_now)
    creator = relationship("User")
    media = relationship(
        "Media",
        primaryjoin="and_(Blog.id==foreign(Media.entity_id), Media.entity_type=='blog')",
        cascade="all, delete-orphan",
        order_by="Media.sort_order"
    )