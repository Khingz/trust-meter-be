from pydantic import (
    BaseModel,
    StringConstraints,
    Field
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
    rating: Annotated[int, Field(ge=1)]
    listing_id: UUID

class ReviewUpdate(ReviewBase):
    pass


class ReviewCommentCreate(BaseModel):
    content: str

class ReviewCommentResponse(BaseModel):
    id: int
    user_id: int
    content: str