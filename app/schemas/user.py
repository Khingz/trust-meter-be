from pydantic import (
    BaseModel,
    EmailStr,
    StringConstraints,
)
from datetime import datetime
from typing import Optional, Annotated

class RegisterUserInput(BaseModel):
    """Schema to create a new user"""
    email: EmailStr
    password: Annotated[
        str, StringConstraints(min_length=3, max_length=64, strip_whitespace=True)
    ]
    name: Annotated[
        str, StringConstraints(min_length=2, max_length=30, strip_whitespace=True)
    ]

class RegisteredUserData(BaseModel):
    """Schema for the user data to be returned after registration"""

    id: str
    email: EmailStr
    name: Optional[str]
    is_admin: bool
    created_at: datetime

class RegisteredUserResponse(BaseModel):
    """Schema for the response to be returned after registration"""
    status: str
    status_code: int
    message: str
    access_token: str
    data: RegisteredUserData


class LoginUserInput(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequestInput(BaseModel):
    email: EmailStr


class PasswordResetInput(BaseModel):
    token: str
    password: Annotated[
        str, StringConstraints(min_length=4, max_length=64, strip_whitespace=True)
    ]

