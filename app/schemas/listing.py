from pydantic import (
    BaseModel
)

from typing import Optional

class ListingBase(BaseModel):
    title: str
    description: str
    category: str
    image: Optional[str] = None
    slug: Optional[str] = None

class ListingCreate(BaseModel):
    url: str

class ListingUpdate(ListingBase):
    pass

