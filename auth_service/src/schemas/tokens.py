from enum import StrEnum

from auth_service.src.dao.tokensDAO import AccessTokensDAO, RefreshTokensDAO


class TokenTypesEnum(StrEnum):
    access = "access"
    refresh = "refresh"


TOKENS_DAOS_MAPPER = {
    TokenTypesEnum.access: AccessTokensDAO,
    TokenTypesEnum.refresh: RefreshTokensDAO,
}
