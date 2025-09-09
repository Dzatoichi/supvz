from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.dao.baseDAO import BaseDAO
from src.models.tokens.access_tokens import AccessTokens
from src.models.tokens.refresh_tokens import RefreshTokens
from src.models.tokens.stateful_tokens import StatefulTokens


class StatefulTokenDAO(BaseDAO[StatefulTokens]):
    def __init__(self):
        super().__init__(model=StatefulTokens)

    async def create_token(self, payload: dict) -> StatefulTokens:
        return await self.create(payload)

    async def get_by_token(self, token: str) -> Optional[StatefulTokens]:
        """Получает токен по строке токена."""
        try:
            stmt = select(self.model).where(self.model.token == token)
            async with self._get_session() as session:
                res = await session.execute(stmt)
                return res.scalars().first()
        except SQLAlchemyError as e:
            raise e

    async def mark_as_used(self, token_id: int) -> Optional[StatefulTokens]:
        """Помечает токен как использованный."""
        return await self.update(token_id, used=True)


class AccessTokensDAO(BaseDAO[AccessTokens]):
    def __init__(self):
        super().__init__(model=AccessTokens)


class RefreshTokensDAO(BaseDAO[RefreshTokens]):
    def __init__(self):
        super().__init__(model=RefreshTokens)
