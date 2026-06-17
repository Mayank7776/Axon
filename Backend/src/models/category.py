from sqlalchemy import Column, String #type: ignore
from src.core.db import Base
import uuid

class BlogCategory(Base):
    __tablename__ = "blog_categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
