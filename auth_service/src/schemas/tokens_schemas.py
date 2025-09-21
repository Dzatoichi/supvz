from enum import StrEnum

from pydantic import BaseModel


class TokenTypesEnum(StrEnum):
    """
    Типы токенов. Эминем.
    """
    access = "access"
    refresh = "refresh"


class TokenSchema(BaseModel):
    """
    Схема для токенов.
    """
    access_token: str
    refresh_token: str
