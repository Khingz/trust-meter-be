from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.baseModel import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class Like(BaseModel):
    __tablename__ = "likes"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    target_id = Column(UUID(as_uuid=True), nullable=False)
    target_type = Column(String, nullable=False) # Type: 'review', 'comment'.

    __table_args__ = (
        UniqueConstraint("user_id", "target_id", "target_type", name="unique_user_like"),
    )

    user = relationship("User")
