from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, EmailStr, SecretStr, StringConstraints, ConfigDict, field_validator, Field

PasswordStr = Annotated[SecretStr, StringConstraints(min_length=8, max_length=128)]


class UserRole(str, Enum):
    """Pydantic model for user's roles ."""

    owner = "owner"
    curator = "curator"
    employee = "employee"


class UserBase(BaseModel):
    """Base Pydantic model for user data"""

    email: EmailStr
    full_name: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class UserLogin(BaseModel):
    """Pydantic model for user login data."""

    email: EmailStr
    password: PasswordStr

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserRegister(UserLogin):
    """Pydantic model for user registration data."""

    password: PasswordStr


class UserUpdate(BaseModel):
    """Pydantic model for user update data."""

    full_name: str | None = None
    phone: str | None = None
    role: UserRole | None = None
    pickup_points: list[int] | None = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserRead(UserBase):
    """Pydantic model for response user data."""

    id: int
    role: UserRole
    pickup_points: list[int] = Field(default_factory=list)
    created_at: datetime


class UserPasswordUpdate(BaseModel):
    """Pydantic model for user update password."""

    current_password: PasswordStr
    new_password: PasswordStr
    confirm_password: PasswordStr

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserResetPassword(BaseModel):
    """Pydantic model for user reset password."""

    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)