from pydantic import (
    BaseModel
)

from typing import Optional

class ReviewBase(BaseModel):
    pass

class ReviewCreate(BaseModel):
    pass

class ReviewUpdate(ReviewBase):
    pass

