from typing import Optional

from sqlalchemy import select

from src.dao.baseDAO import BaseDAO
from src.models.tokens.access_tokens import AccessTokens
from src.models.tokens.refresh_tokens import RefreshTokens
from src.models.tokens.stateful_tokens import StatefulTokens
from src.utils.exceptions import InvalidTokenException


class StatefulTokenDAO(BaseDAO[StatefulTokens]):
    def __init__(self):
        super().__init__(model=StatefulTokens)

    async def create_token(self, payload: dict) -> StatefulTokens:
        return await self.create(payload)

    @BaseDAO.with_exception
    async def get_by_token(self, token: str) -> Optional[StatefulTokens]:
        """Получает токен по строке токена."""
        stmt = select(self.model).where(self.model.token == token)
        async with self._get_session() as session:
            res = await session.execute(stmt)
            return res.scalars().first()

    async def mark_as_used(self, token_id: int) -> Optional[StatefulTokens]:
        """Помечает токен как использованный."""
        return await self.update(token_id, used=True)


class AccessTokensDAO(BaseDAO[AccessTokens]):
    def __init__(self):
        super().__init__(model=AccessTokens)


class RefreshTokensDAO(BaseDAO[RefreshTokens]):
    def __init__(self):
        super().__init__(model=RefreshTokens)

    @BaseDAO.with_exception
    async def get_token_by_token_hash(self, token_hash: str) -> Optional[RefreshTokens]:
        async with self._get_session() as session:
            stmt = select(self.model).where(self.model.token_hash == token_hash)
            res = await session.execute(stmt)
            return res.scalars().first()

    @BaseDAO.with_exception
    async def set_token_revoked(self, token_hash: str) -> None:
        async with self._get_session() as session:
            stmt = select(self.model).where(self.model.token_hash == token_hash)
            res = await session.execute(stmt)
            token_obj = res.scalar_one_or_none()
            if not token_obj:
                raise InvalidTokenException("Токен не найден")
            token_obj.revoked = True
            await session.commit()
