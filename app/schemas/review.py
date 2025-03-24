from pydantic import BaseModel
from typing import Optional

# Review Create Schema
class ReviewCreate(BaseModel):
    rating: int  # Rating between 1 and 5
    review_text: str
    multimedia: Optional[str] = None  # Optional multimedia URL or file path

    class Config:
        orm_mode = True  # Allows Pydantic models to work with SQLAlchemy models

# Review Update Schema
class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    review_text: Optional[str] = None
    multimedia: Optional[str] = None  # Optional multimedia URL or file path

    class Config:
        orm_mode = True  # Allows Pydantic models to work with SQLAlchemy models

# Review Response Schema (for retrieving data)
class ReviewResponse(ReviewCreate):
    id: int  # Assuming the `id` is an integer
    product_id: str  # The ID of the related product

    class Config:
        orm_mode = True
