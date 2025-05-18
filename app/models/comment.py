from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.models.baseModel import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class ReviewComment(BaseModel):
    __tablename__ = "review_comments"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    review_id = Column(UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)

    user = relationship("User")
