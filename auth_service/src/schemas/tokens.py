from enum import StrEnum

from pydantic import BaseModel

from src.dao.tokensDAO import AccessTokensDAO, RefreshTokensDAO


class TokenTypesEnum(StrEnum):
    access = "access"
    refresh = "refresh"


class TokenResponse(BaseModel):
    access_token: str


TOKENS_DAOS_MAPPER = {
    TokenTypesEnum.access: AccessTokensDAO,
    TokenTypesEnum.refresh: RefreshTokensDAO,
}
