from enum import StrEnum

from pydantic import BaseModel


class TokenTypesEnum(StrEnum):
    access = "access"
    refresh = "refresh"


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
