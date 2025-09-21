from datetime import datetime, timezone
from typing import Optional, Tuple
from uuid import UUID

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.security.hash_helper import hash_helper
from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import UserLogin, UserRead, UserRegister, UserRole, UserAuthRequest
from src.services.token_service import JWTTokensService, StatefulTokenService
from src.core.security.permissions import PermissionEnum, get_permissions_for_role
from src.models.users.users import Users

security = HTTPBearer()


class AuthService:
    async def register_user(
            self,
            data: UserRegister,
            repo: UsersDAO,
    ) -> UserRead:
        """Регистрация пользователя."""
        user = await repo.get_user_by_email(data.email)
        if user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists")

        hashed_password = hash_helper.hash(data.password)
        payload = {
            "email": data.email,
            "phone_number": data.phone_number,
            "name": data.name,
            "hashed_password": hashed_password,
        }
        user = await repo.create(payload)
        return UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            created_at=user.created_at,
        )

    async def login_user(
            self,
            credentials: UserLogin,
            repo: UsersDAO,
            token_service: JWTTokensService,
    ) -> tuple[str, str]:
        """Авторизация пользователя."""
        user = await repo.get_user_by_email(credentials.email)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        if not hash_helper.verify_password(plain_password=credentials.password, hashed_password=user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid password")

        refresh_token = await token_service.create_token(
            token_type="refresh",
            user_id=user.id,
        )
        access_token = await token_service.create_token(
            token_type="access",
            user_id=user.id,
        )

        return (access_token, refresh_token)

    async def authorize_user(
            self,
            auth_request: UserAuthRequest,  # Изменяем параметр на схему
            token_service: JWTTokensService,
            users_dao: UsersDAO,
    ) -> Tuple[UserRole, list[PermissionEnum]]:
        """
        Авторизация пользователя по access токену.
        Валидирует токен, получает пользователя и возвращает его роль и permissions.
        """
        # Используем переданные зависимости или инициализируем стандартные
        token_service = token_service or self.token_service
        users_dao = users_dao or self.users_dao

        # Если зависимости не предоставлены, пытаемся создать их через Depends
        if token_service is None:
            from src.utils.dependencies import get_jwt_tokens_service
            token_service = get_jwt_tokens_service()

        if users_dao is None:
            from src.utils.dependencies import get_users_dao
            users_dao = get_users_dao()

        token = auth_request.access_token  # Берем токен из схем

        # Валидация токена
        try:
            token_payload = await token_service.validate_token(
                token=token,
                token_type="access"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        # Получение пользователя
        user_id = token_payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        user = await users_dao.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Получение permissions для роли
        permissions = get_permissions_for_role(user.role)

        return user.role, permissions

    async def reset_password(
            self,
            token: str,
            new_password: str,
            token_service: StatefulTokenService,
            repo: UsersDAO,
    ) -> bool:
        """Сброс пароля пользователя."""
        token_data = await token_service.get_reset_token_data(token)

        if not token_data:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

        if token_data.used:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token already used")

        if token_data.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token expired")

        hashed_password = hash_helper.hash(new_password)
        result = await repo.set_password(user_id=token_data.user_id, hashed_password=hashed_password)
        await token_service.mark_token_as_used(token_data)

        return result

    # TODO: доделать после реализации notification service
    async def forgot_password(
            self,
            user_email: str,
            repo: UsersDAO,
            token_service: StatefulTokenService,
    ) -> str:
        """Генерирует токен сброса пароля и инициирует отправку email через notification_service."""

        user = await repo.get_user_by_email(user_email)

        if user:
            token = await token_service.create_stateful_token(user.id)

            # Интеграция с notification_service (пока заглушка)
            # reset_url = f"https://frontend.example.com/reset-password?token={token}"
            #
            # отправка через раббит в notification service

        return token

    async def logout_user(
            self,
            refresh_token: str,
            access_token: str,
            token_service: JWTTokensService,
    ) -> bool:
        """Выход пользователя."""
        await token_service.revoke_token(token=refresh_token, token_type="refresh")
        await token_service.revoke_token(token=access_token, token_type="access")

        return True