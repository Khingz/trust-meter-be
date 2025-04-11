from sqlalchemy import Column, String, Text
from app.models.baseModel import BaseModel
from sqlalchemy.orm import relationship

class Listing(BaseModel):
    __tablename__ = "listings"

    name = Column(String, index=True)
    category = Column(String)
    description = Column(Text, nullable=True)
    listing_url = Column(String)
    image = Column(String, nullable=True)
    slug = Column(String, unique=True, index=True)
    
    reviews = relationship("Review", back_populates="listing", cascade="all, delete")