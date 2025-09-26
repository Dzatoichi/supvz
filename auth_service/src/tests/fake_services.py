from fastapi import Response


class FakeUsersDAO:
    """
    Класс-заглушка (mock) для DAO пользователей.
    """

    pass


class FakeAuthService:
    """
    Класс-заглушка (mock) для сервиса аутентификации пользователей.
    """

    async def register_user(self, data, repo):
        """
        Метод регистрации пользователя.
        """
        return {
            "id": 1,
            "email": data.email,
            "name": data.name,
            "role": "owner",
            "created_at": "2024-01-01T00:00:00",
        }

    async def login_user(self, credentials, repo, token_service):
        """
        Метод аутентификации пользователя.
        """
        return {"access_token": "access_token", "refresh_token": "refresh_token"}

    async def forgot_password(self, user_email, repo, token_service):
        """
        Метод запроса для изменения пароля, если пользователь забыл пароль.
        """
        return None

    async def reset_password(self, token, new_password, token_service, repo):
        """
        Метод сброса пароля пользователя.
        """
        return None

    async def logout_user(
        self,
        refresh_token: str,
        response: Response,
        token_service,
    ):
        """
        Метод завершения сессии/выхода пользователя.
        """
        return {"description": "Logged out successfully"}


class FakeJWTTokensService:
    """
    Класс-заглушка (mock) для сервиса работы с JWT токенами.
    """

    async def refresh_token(self, refresh_token):
        return {"refresh_token": "refresh", "access_token": "access"}


class FakeStatefulTokenService:
    """
    Класс-заглушка (mock) для stateful сервиса токенов.
    """

    pass
