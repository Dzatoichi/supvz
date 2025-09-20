from enum import StrEnum

from pydantic import BaseModel

from src.dao.tokensDAO import RefreshTokensDAO


class TokenTypesEnum(StrEnum):
    access = "access"
    refresh = "refresh"


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginSchema(BaseModel):
    access_token: str


TOKENS_DAOS_MAPPER = {
    TokenTypesEnum.refresh: RefreshTokensDAO,
}
