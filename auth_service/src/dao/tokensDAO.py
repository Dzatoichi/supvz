from typing import Optional

from sqlalchemy import select

from src.dao.baseDAO import BaseDAO
from src.models.tokens.refresh_tokens import RefreshTokens
from src.models.tokens.stateful_tokens import StatefulTokens
from src.utils.exceptions import InvalidTokenException


class StatefulTokenDAO(BaseDAO[StatefulTokens]):
    """
    Класс, наследующий базовый DAO для работы с сущностями stateful-токенов.
    """
    def __init__(self):
        super().__init__(model=StatefulTokens)

    async def create_token(self, payload: dict) -> StatefulTokens:
        """
        Метод создания токена.
        """
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


class RefreshTokensDAO(BaseDAO[RefreshTokens]):
    """
    Класс, наследующий базовый DAO для работы с сущностями refresh-токенов.
    """
    def __init__(self):
        super().__init__(model=RefreshTokens)

    @BaseDAO.with_exception
    async def get_token_by_token_hash(self, token_hash: str) -> Optional[RefreshTokens]:
        """
        Метод для получения токена по хеш-строке.
        """
        async with self._get_session() as session:
            stmt = select(self.model).where(self.model.token_hash == token_hash)
            res = await session.execute(stmt)
            return res.scalars().first()

    @BaseDAO.with_exception
    async def set_token_revoked(self, token_hash: str) -> None:
        """
        Метод для обозначения токена, как отозванного.
        """
        async with self._get_session() as session:
            stmt = select(self.model).where(self.model.token_hash == token_hash)
            res = await session.execute(stmt)
            token_obj = res.scalar_one_or_none()
            if not token_obj:
                raise InvalidTokenException("Токен не найден")
            token_obj.revoked = True
            await session.commit()
