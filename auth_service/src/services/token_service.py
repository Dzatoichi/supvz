from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from src.core.security.hash_helper import hash_helper
from src.core.security.token_handler import TokenHandler
from src.dao.tokensDAO import StatefulTokenDAO
from src.models.tokens.stateful_tokens import StatefulTokens
from src.schemas.tokens import TOKENS_DAOS_MAPPER, TokenTypesEnum
from src.utils.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
)


class JWTTokensService:
    """JWT tokens service."""

    async def create_token(
            self,
            token_type: TokenTypesEnum,
            user_id: UUID,
    ) -> str:
        """Method to create access or refresh token."""
        token_handler = TokenHandler(token_type=token_type)
        repo = TOKENS_DAOS_MAPPER[token_type]

        token, expires_at = token_handler.sign_jwt(user_id=user_id)

        token_hash = hash_helper.hash(plain_str=token)
        payload = {
            "user_id": user_id,
            "token_hash": token_hash,
            "issued_at": datetime.now(timezone.utc),
            "expires_at": expires_at,
        }
        await repo.create(payload=payload)
        return token

    async def revoke_token(
            self,
            token: str,
            token_type: TokenTypesEnum,
    ) -> bool:
        """Method to revoke token."""
        repo = TOKENS_DAOS_MAPPER[token_type]

        token_hash = hash_helper.hash(plain_str=token)
        await repo.set_token_revoked(token_hash=token_hash)

        return True

    async def refresh_token(
            self,
            refresh_token: str,
    ) -> dict[str, str]:
        """Method to refresh token with rotation of tokens."""
        token_payload = await self.validate_token(
            token=refresh_token,
            token_type=TokenTypesEnum.refresh,
        )

        access_token = await self.create_token(
            token_type=TokenTypesEnum.access,
            user_id=token_payload.get("user_id"),
        )

        await self.revoke_token(
            token=refresh_token,
            token_type=TokenTypesEnum.refresh,
        )

        new_refresh_token = await self.create_token(
            token_type=TokenTypesEnum.refresh,
            user_id=token_payload.get("user_id"),
        )
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
        }

    async def validate_token(
            self,
            token: str,
            token_type: TokenTypesEnum,
    ) -> dict:
        repo = TOKENS_DAOS_MAPPER[token_type]
        token_handler = TokenHandler(token_type=token_type)

        token_payload = token_handler.decode_jwt(token=token)
        if not token_payload:
            raise InvalidTokenException("Invalid token.")

        if token_payload.get("exp") < datetime.now(timezone.utc):
            raise TokenExpiredException("Token expired.")

        token_hash = hash_helper.hash(plain_str=token)
        token_info = await repo.get_token_by_token_hash(token_hash=token_hash)

        if not token_info or token_info.get("revoked"):
            raise InvalidTokenException("Invalid token.")

        return token_payload


class StatefulTokenService:
    def __init__(self, dao: StatefulTokenDAO):
        self.dao = dao

    async def create_stateful_token(self, user_id: int, expires_in_minutes: int = 15) -> str:
        """Создаёт токен и возвращает его строку."""
        token_obj = self.dao.create_token(user_id, expires_in_minutes)
        return await token_obj.token

    async def get_reset_token_data(self, token: str) -> Optional[StatefulTokens]:
        """Получает данные токена и проверяет валидность."""
        return await self.dao.validate_token(token)

    async def mark_token_as_used(self, token_obj: StatefulTokens):
        """Помечает как использованный."""
        await self.dao.mark_as_used(token_obj.id)
