from sqlalchemy import ( #type:ignore
    Column,
    String,
    DateTime,
    ForeignKey,
    JSON
) 
from sqlalchemy.orm import relationship #type:ignore
from datetime import datetime, timezone
from src.core.db import Base
import uuid


def utc_now():
    return datetime.now(timezone.utc)


class NutritionChart(Base):
    __tablename__ = "nutrition_charts"

    id = Column(String(36),primary_key=True,default=lambda: str(uuid.uuid4()))
    created_by = Column(String(36),ForeignKey("users.id", ondelete="SET NULL"),nullable=True)
    title = Column(String(100),nullable=False)
    slug = Column(String(100),unique=True,nullable=True)
    description = Column(String(500),nullable=True)
    image_url = Column(String(1000),nullable=True)
    diet_plan = Column(JSON,nullable=False)
    created_at = Column(DateTime(timezone=True),default=utc_now)
    updated_at = Column(DateTime(timezone=True),default=utc_now,onupdate=utc_now)
    
    # relationship
    creator = relationship("User",back_populates="nutrition_charts")