from enum import StrEnum

from pydantic import BaseModel


class TokenTypesEnum(StrEnum):
    """
    Перечисление типов токена.
    """

    access = "access"
    refresh = "refresh"


class TokenSchema(BaseModel):
    """
    Схема токенов.
    """

    access_token: str
    refresh_token: str
