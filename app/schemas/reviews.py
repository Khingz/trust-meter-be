from pydantic import (
    BaseModel,
    StringConstraints,
)
from typing import Optional, Annotated
from uuid import UUID


from typing import Optional

class ReviewBase(BaseModel):
    pass

class ReviewCreate(BaseModel):
    comment: Annotated[
        str, StringConstraints(min_length=4, strip_whitespace=True)
    ]
    rating: int = 0
    listing_id: UUID

class ReviewUpdate(ReviewBase):
    pass

