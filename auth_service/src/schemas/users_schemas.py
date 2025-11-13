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

from src.core.security.permissions import PermissionEnum
from src.core.security.permissions.role_permissions import get_permissions_for_role

str = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class UserRoleEnum(str, Enum):
    """
    Перечисление ролей пользователя.
    """

    administrator = "administrator"
    owner = "owner"
    curator = "curator"
    employee = "employee"
    intern = "intern"
    handyman = "handyman"


class SubscriptionEnum(Enum):
    """
    Перечисление статусов подписки.
    """

    paid = "paid"
    test = "test"
    expired = "expired"


class UserBaseSchema(BaseModel):
    """
    Базовая схема пользователя.
    """

    email: EmailStr

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

    id: int
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserReadSchema(UserBaseSchema):
    """
    Схема получения пользователя.
    """

    id: int
    role: UserRoleEnum
    subscription: SubscriptionEnum
    permissions: list[PermissionEnum] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    @model_validator(mode="after")
    def set_permissions(self) -> "UserReadSchema":
        self.permissions = get_permissions_for_role(self.role)
        return self


class UserAuthRequestSchema(BaseModel):
    """
    Схема для принятия авторизационного запроса(токена).
    """

    access_token: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class PasswordResetConfirmSchema(BaseModel):
    """
    Схема подтверждения сброса пароля пользователя.
    """

    token: str
    new_password: str
    confirm_new_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "PasswordResetConfirmSchema":
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
