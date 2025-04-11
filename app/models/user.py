from sqlalchemy import Column, Integer, String, Boolean
from app.models.baseModel import BaseModel
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String, index=True)
    email = Column(String, unique=False, index=True)
    password = Column(String, nullable=False)
    password_reset_token = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    
    reviews = relationship("Review", back_populates="user")