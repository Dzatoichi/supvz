from datetime import datetime
from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel, EmailStr, SecretStr, StringConstraints, ConfigDict, field_validator, Field, \
    model_validator

PasswordStr = Annotated[SecretStr, StringConstraints(min_length=8, max_length=128)]


class UserRole(str, Enum):
    """Pydantic model for user's roles ."""

    owner = "owner"
    administrator = "administrator"
    manager = "manager"
    helper = "helper"
    intern = "intern"


class UserBase(BaseModel):
    """Base Pydantic model for user data"""
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    email: EmailStr
    full_name: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()


class UserLogin(BaseModel):
    """Pydantic model for user login data."""

    email: EmailStr
    password: PasswordStr


class UserRegister(UserLogin):
    """Pydantic model for user registration data."""

    confirm_password: PasswordStr


class UserUpdate(BaseModel):
    """Pydantic model for user update data."""

    full_name: str | None = None
    phone: str | None = None
    role: UserRole | None = None
    pickup_points: list[int] | None = Field(default_factory=list)


class UserRead(UserBase):
    """Pydantic model for response user data."""

    id: int
    role: UserRole
    pickup_points: list[int] = Field(default_factory=list)
    created_at: datetime


class PasswordResetConfirm(BaseModel):
    """Pydantic model for password reset confirmation data."""

    token: str
    new_password: PasswordStr
    confirm_new_password: PasswordStr

    @model_validator(mode="after")
    def check_passwords_match(self) -> "PasswordResetConfirm":
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords do not match")
        return self


class UserPasswordUpdate(BaseModel):
    """Pydantic model for user update password."""

    current_password: PasswordStr
    new_password: PasswordStr
    confirm_password: PasswordStr

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserPasswordUpdate":
        if self.new_password != self.confain_new_password:
            raise ValueError("Passwords do not match")
        return self


class UserForgotPassword(BaseModel):
    """Pydantic model for user reset password."""

    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()


class TokenResponse(BaseModel):
    """Pydantic model for response access token."""

    access_token: str
    token_type: str = "bearer"
