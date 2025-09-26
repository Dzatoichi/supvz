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
    """
    Перечисление ролей пользователя.
    """

    administrator = "administrator"
    owner = "owner"
    test_owner = "test_owner"
    curator = "curator"
    employee = "employee"
    intern = "intern"
    handyman = "handyman"


class UserBaseSchema(BaseModel):
    """
    Базовая схема пользователя.
    """

    email: EmailStr
    name: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserLoginSchema(BaseModel):
    """
    Схема аутентификации пользователя.
    """

    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserRegisterSchema(UserLoginSchema):
    """
    Схема регистрации пользователя.
    """

    confirm_password: str
    name: str
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        """
        Функция валиадации номера телефона.
        """
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError("Invalid phone number")
        return values

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegisterSchema":
        """
        Метод проверки на совпадение пароля.
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserUpdateSchema(BaseModel):
    """
    Схема изменения пользователя.
    """

    full_name: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserReadSchema(UserBaseSchema):
    """
    Схема получения пользователя.
    """

    id: int
    role: UserRole
    created_at: datetime


class PasswordResetConfirmSchema(BaseModel):
    """
    Схема подтверждения сброса пароля пользователя.
    """

    token: str
    new_password: str
    confirm_new_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "PasswordResetConfirmSchema":
        """
        Метод проверки на совпадение пароля.
        """
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords do not match")
        return self


class UserPasswordUpdateSchema(BaseModel):
    """
    Схема изменения пароля пользователя.
    """

    current_password: str
    new_password: str
    confirm_password: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserPasswordUpdateSchema":
        """
        Метод проверки на совпадение пароля.
        """
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserForgotPasswordSchema(BaseModel):
    """
    Схема запроса на изменение пароля в случае, если пользователь забыл пароль.
    """

    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return v.lower()

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
