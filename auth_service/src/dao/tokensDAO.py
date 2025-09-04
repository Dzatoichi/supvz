import secrets
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.dao.baseDAO import BaseDAO
from src.models.tokens.stateful_tokens import StatefulTokens


class StatefulTokenDAO(BaseDAO[StatefulTokens]):
    def __init__(self):
        super().__init__(model=StatefulTokens)

    async def create_token(self, user_id: int, expires_in_minutes: int = 15) -> StatefulTokens:
        """Генерирует и сохраняет новый токен для пользователя."""
        token_str = secrets.token_urlsafe(16)
        expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)

        payload = {
            "token": token_str,
            "user_id": user_id,
            "expires_at": expires_at,
            "used": False,
        }

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

    async def validate_token(self, token: str) -> Optional[StatefulTokens]:
        """Метод для проверки валидности."""
        token_obj = await self.get_by_token(token)
        if not token_obj or token_obj.used or token_obj.expires_at < datetime.utcnow():
            return None
        return token_obj
