from datetime import datetime

from fastapi import HTTPException, status

from src.dao.usersDAO import UsersDAO
from src.services.token_service import StatefulTokenService

from src.schemas.users_schemas import UserBase


class AuthService:
    def __init__(self, auth_repo: UsersDAO, token_service: StatefulTokenService | None = None):
        self.auth_repo = auth_repo
        self.token_service = token_service

    async def register_user(self, user_in):
        pass

    async def login_user(self, credentials):
        pass

    async def reset_password(self, token, new_password):
        """Сбрасывает пароль пользователя"""

        token_data = await self.token_service.get_reset_token_data(token)

        if not token_data:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

        if token_data.used:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token already used")

        if token_data.expires_at < datetime.now():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token expired")

        # Обновляем пароль и помечаем токен как использованный
        result = await self.auth_repo.set_password(token_data.id, new_password)
        await self.token_service.mark_token_as_used(token_data)

        return result

    async def forgot_password(self, user: UserBase):
        """
        Генерирует токен сброса пароля и инициирует отправку email через notification_service.

        Args:
            user: Объект пользователя, для которого запрашивается сброс пароля

        Returns:
            Сообщение о результате операции (всегда успешное)
        """

        # Генерация токена
        token = self.token_service.create_stateful_token(user)

        # Интеграция с notification_service
        # reset_url = f"{self.config.frontend_base_url}/reset-password?token={token}"
        # await self.notification_service.send_password_reset(
        #     email=user.email,
        #     reset_url=reset_url
        # )

        return None

    async def get_by_email(self, user_email: str):
        """Get a user by e-mail."""
        user_or_none = await self.auth_repo.get_by_email(user_email)

        return user_or_none
