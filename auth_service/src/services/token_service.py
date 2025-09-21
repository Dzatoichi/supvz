import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.core.security.hash_helper import hash_helper
from src.core.security.token_handler import TokenHandler
from src.dao.tokensDAO import RefreshTokensDAO, StatefulTokenDAO
from src.models.tokens.stateful_tokens import StatefulTokens
from src.schemas.tokens import TOKENS_DAOS_MAPPER, TokenTypesEnum
from src.settings.config import settings
from src.utils.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
)


class JWTTokensService:
    """JWT tokens service."""

    def __init__(self, repo: RefreshTokensDAO | None = None):
        self.repo = repo

    async def create_token(
        self,
        token_type: TokenTypesEnum,
        user_id: int,
    ) -> str:
        """Method to create access or refresh token."""
        token_handler = TokenHandler(token_type=token_type)
        token, expires_at = token_handler.sign_jwt(user_id=user_id)

        if token_type == TokenTypesEnum.refresh:
            repo = TOKENS_DAOS_MAPPER[token_type]()
            token_hash = hash_helper.hash_token(token=token)
            print(token_hash)
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
    ) -> bool:
        """Method to revoke token."""

        token_hash = hash_helper.hash_token(token=token)
        await self.repo.set_token_revoked(token_hash=token_hash)

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
        token_handler = TokenHandler(token_type=token_type)

        token_payload = token_handler.decode_jwt(token=token)
        if not token_payload:
            raise InvalidTokenException("Invalid token.")

        if datetime.fromtimestamp(
            token_payload.get("exp"), tz=timezone.utc
        ) < datetime.now(timezone.utc):
            raise TokenExpiredException("Token expired.")

        token_hash = hash_helper.hash_token(token=token)
        token_info = await self.repo.get_token_by_token_hash(token_hash=token_hash)

        if not token_info or token_info.revoked:
            raise InvalidTokenException("Invalid token.")

        return token_payload


class StatefulTokenService:
    def __init__(self, dao: StatefulTokenDAO | None = None):
        self.dao = dao

    async def create_stateful_token(
        self,
        user_id: int,
    ):
        """Создаёт токен и возвращает его строку."""

        token_str = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.STATEFUL_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "token": token_str,
            "user_id": user_id,
            "expires_at": expires_at,
            "used": False,
        }
        return await self.dao.create(payload)

    async def get_reset_token_data(self, token: str) -> Optional[StatefulTokens]:
        """Получает данные токена и проверяет валидность."""
        return await self.validate_token(token)

    async def mark_token_as_used(
        self,
        token_obj: StatefulTokens,
    ) -> None:
        """Помечает как использованный."""
        await self.dao.mark_as_used(token_obj.id)

    async def validate_token(
        self,
        token: str,
    ) -> Optional[StatefulTokens]:
        """Метод для проверки валидности."""
        token_obj = await self.dao.get_by_token(token)
        if (
            not token_obj
            or token_obj.used
            or token_obj.expires_at < datetime.now(timezone.utc)
        ):
            return None
        return token_obj
