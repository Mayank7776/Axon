from sqlalchemy import Column, String, Boolean #type: ignore
from sqlalchemy.orm import relationship #type: ignore
from src.core.db import Base
import uuid


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # relationship
    users = relationship("User", back_populates="role")
    