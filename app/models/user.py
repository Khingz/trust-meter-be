from sqlalchemy import Column, Integer, String, Boolean
from app.models.baseModel import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String, index=True)
    email = Column(String, unique=False, index=True)
    password = Column(String, nullable=False)
    password_reset_token = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)