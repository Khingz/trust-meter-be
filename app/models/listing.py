from sqlalchemy import Column, Integer, String, Boolean, Text
from app.models.baseModel import BaseModel

class Listing(BaseModel):
    __tablename__ = "listings"

    name = Column(String, index=True)
    category = Column(String)
    description = Column(Text, nullable=True)
    listing_url = Column(String)
    image = Column(String, nullable=True)
    slug = Column(String, unique=True, index=True)