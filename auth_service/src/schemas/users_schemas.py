from datetime import datetime
from enum import Enum
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    StringConstraints,
    field_validator,
    model_validator,
)

from src.schemas.enums import PositionSourceEnum

str = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class SubscriptionEnum(Enum):
    """
    Перечисление статусов подписки.
    """

    paid = "paid"
    test = "test"
    expired = "expired"


class StatusResponseSchema(BaseModel):
    """Схема для возврата текстового ответа."""

    status: Literal["ok", "error"] = "ok"
    message: str | None = None


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
    register_token: Annotated[str, StringConstraints(min_length=8, max_length=512)] | None = None

    position_id: int | None = None
    position_source: PositionSourceEnum | None = None

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegisterSchema":
        """
        Метод проверки на совпадение пароля.
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    @model_validator(mode="after")
    def validate_registration_fields(self) -> "UserRegisterSchema":
        """
        Проверка:
        1) Если position_id указан, то обязательно position_source и наоборот.
        2) Должен быть хотя бы один способ регистрации:
           - invite_token или
           - position_id + position_source
        """
        if (self.position_id is None) != (self.position_source is None):
            raise ValueError("Необходимо указать и position_id, и position_source.")

        if not self.register_token and self.position_id is None:
            raise ValueError("Необходимо указать либо 'register_token', либо 'position_id' + 'position_source'.")

        return self


class UserUpdateSchema(UserBaseSchema):
    """
    Схема изменения пользователя.
    """

    pass


class UserUpdateMeSchema(UserBaseSchema):
    """
    Схема для изменения собственных данных пользователя
    """

    pass


class UserReadSchema(UserBaseSchema):
    """
    Схема получения пользователя.
    """

    id: int
    subscription: SubscriptionEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


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


class UpdateUserPermissionsSchema(BaseModel):
    permission_ids: list[int]


class UpdateUsersPermissionsSchema(BaseModel):
    """
    Схема для обновления списка прав у всех юзеров,
    которые подаются на вход
    """

    users: list[int]
    new_permission_ids: list[int]


# TODO: начать использовать position
class UserRegisterEmployeeSchema(BaseModel):
    """
    Схема запроса для генерации JWT register token, который используется для регистрации сотрудников.
    """

    pvz_id: int
    owner_id: int
    position_id: int
    position_source: PositionSourceEnum = PositionSourceEnum.system

    model_config = ConfigDict(from_attributes=True)
