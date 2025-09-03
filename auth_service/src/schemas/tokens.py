from enum import StrEnum

from auth_service.src.dao.tokensDAO import AccessTokensDAO, RefreshTokensDAO
from pydantic import BaseModel


class TokenTypesEnum(StrEnum):
    access = "access"
    refresh = "refresh"


class TokenResponse(BaseModel):
    access_token: str


TOKENS_DAOS_MAPPER = {
    TokenTypesEnum.access: AccessTokensDAO,
    TokenTypesEnum.refresh: RefreshTokensDAO,
}
