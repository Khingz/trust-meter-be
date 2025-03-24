from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID as a unique identifier
    name = Column(String, index=True)
    brand = Column(String)
    category = Column(String)
    description = Column(Text)
    image = Column(String, nullable=True)  # Optional field for product image
    slug = Column(String, unique=True, index=True)
    
    reviews = relationship("Review", back_populates="product")
    
    def __repr__(self):
        return f"<Product(name={self.name}, brand={self.brand}, category={self.category})>"
