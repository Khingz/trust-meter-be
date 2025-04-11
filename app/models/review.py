from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from app.models.baseModel import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Review(BaseModel):
    __tablename__ = "reviews"
    
    product_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    product = relationship("Lisings", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    