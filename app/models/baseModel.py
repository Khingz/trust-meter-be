from app.db.database import Base
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, func, UUID

class BaseModel(Base):
    """Base model for all models"""
    __abstract__ = True

    # id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


