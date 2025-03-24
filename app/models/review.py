from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)  # Rating from 1-5
    review_text = Column(Text)
    multimedia = Column(String, nullable=True)  # Optional multimedia URL or file path
    product_id = Column(String, ForeignKey("products.id"))
    
    product = relationship("Product", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(rating={self.rating}, product_id={self.product_id})>"
