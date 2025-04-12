from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from app.models.baseModel import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Review(BaseModel):
    __tablename__ = "reviews"
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    listings = relationship("Listing", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    