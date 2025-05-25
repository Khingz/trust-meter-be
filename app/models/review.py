from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.baseModel import BaseModel
from sqlalchemy.orm import relationship, foreign, remote
from app.models.like import Like
from sqlalchemy.sql import and_
from sqlalchemy.dialects.postgresql import UUID

class Review(BaseModel):
    __tablename__ = "reviews"
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    likes = relationship(
        "Like",
        primaryjoin=lambda: and_(
        foreign(Like.target_id) == Review.id,
        Like.target_type == "review"
    ),
        viewonly=True
    )
    listings = relationship("Listing", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    comments = relationship("ReviewComment", backref="review", cascade="all, delete-orphan")
    