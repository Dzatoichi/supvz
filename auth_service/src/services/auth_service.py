from datetime import datetime, timezone

from fastapi import HTTPException, status

from src.dao.usersDAO import UsersDAO
from src.services.token_service import StatefulTokenService


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

        if token_data.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token expired")

        # Обновляем пароль и помечаем токен как использованный
        result = await self.auth_repo.set_password(token_data.user_id, new_password)
        await self.token_service.mark_token_as_used(token_data)

        return result

    async def forgot_password(self, user_email: str):
        """
        Генерирует токен сброса пароля и инициирует отправку email через notification_service.

        Args:
            user_email: Почта пользователя, для которого запрашивается сброс пароля

        Returns:
            Сообщение о результате операции (всегда успешное)
        """

        try:
            user = await self.auth_repo.get_user_by_email(user_email)

            if user:
                # Генерация токена
                token = await self.token_service.create_stateful_token(user.id)

                # Интеграция с notification_service (пока заглушка)
                reset_url = f"https://frontend.example.com/reset-password?token={token}"
                print(f"[EMAIL-FAKE] reset link={reset_url} email={user.email}")
                # try:
                #     await self.notification_service.send_password_reset(
                #         email=user.email,
                #         reset_url=reset_url
                #     )
                # except Exception as e:
                #     logger.error(f"Ошибка при отправке email: {e}")

        except Exception as e:
            print(f"Ошибка при forgot_password: {e}")

        return None

    async def get_by_email(self, user_email: str):
        """Get a user by e-mail."""
        user = await self.auth_repo.get_user_by_email(user_email)

        return user
