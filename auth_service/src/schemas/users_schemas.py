import re
from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    StringConstraints,
    field_validator,
    model_validator,
)

str = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class UserRole(str, Enum):
    """Pydantic model for user's roles ."""

    owner = "owner"
    curator = "curator"
    employee = "employee"


class UserBase(BaseModel):
    """Base Pydantic model for user data"""

    email: EmailStr
    name: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserLogin(BaseModel):
    """Pydantic model for user login data."""

    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserRegister(UserLogin):
    """Pydantic model for user registration data."""

    confirm_password: str
    name: str
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegister":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(BaseModel):
    """Pydantic model for user update data."""

    full_name: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserRead(UserBase):
    """Pydantic model for response user data."""

    id: int
    role: UserRole
    created_at: datetime


class PasswordResetConfirm(BaseModel):
    """Pydantic model for password reset confirmation data."""

    token: str
    new_password: str
    confirm_new_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "PasswordResetConfirm":
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords do not match")
        return self


class UserPasswordUpdate(BaseModel):
    """Pydantic model for user update password."""

    current_password: str
    new_password: str
    confirm_password: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserPasswordUpdate":
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserForgotPassword(BaseModel):
    """Pydantic model for user reset password."""

    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserLogout(BaseModel):
    """Pydantic model for user logout."""

    refresh_token: str
    access_token: str
