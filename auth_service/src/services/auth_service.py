from datetime import datetime, timezone

from fastapi import Response

from src.core.security.hash_helper import hash_helper
from src.core.security.permissions import PermissionEnum, has_permission
from src.dao.permissionsDAO import PermissionsDAO
from src.dao.usersDAO import UsersDAO
from src.schemas.tokens_schemas import TokenTypesEnum
from src.schemas.users_schemas import (
    UserLoginSchema,
    UserReadSchema,
    UserRegisterSchema,
)
from src.services.token_service import JWTTokensService, StatefulTokenService
from src.utils.exceptions import (
    IncorrectPasswordException,
    InvalidTokenException,
    PermissionDeniedException,
    TokenExpiredException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


class AuthService:
    """
    Класс сервиса аутентификации.
    """

    def __init__(self, db_helper):
        self.db_helper = db_helper

    async def register_user(
        self,
        data: UserRegisterSchema,
        user_repo: UsersDAO,
        perm_repo: PermissionsDAO,
    ) -> UserReadSchema:
        """
        Метод регистрации пользователя.
        """
        user = await user_repo.get_user_by_email(email=data.email)
        if user:
            raise UserAlreadyExistsException("User already exists")

        hashed_password = hash_helper.hash(plain_str=data.password)
        payload = {
            "email": data.email,
            "hashed_password": hashed_password,
        }

        permissions = await perm_repo.get_permissions_by_position(position_id=data.position_id)

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                user = await user_repo.create_user(
                    payload=payload,
                    session=session,
                )
                await user_repo.assign_permissions(
                    user_id=user.id,
                    permissions=permissions,
                    session=session,
                )

        return UserReadSchema.model_validate(user)

    async def login_user(
        self,
        credentials: UserLoginSchema,
        repo: UsersDAO,
        token_service: JWTTokensService,
    ) -> tuple[str, str]:
        """
        Метод аутентификации пользователя.
        """
        user = await repo.get_user_by_email(email=credentials.email)
        if not user:
            raise UserNotFoundException("User not found")

        if not hash_helper.verify_password(plain_password=credentials.password, hashed_password=user.hashed_password):
            raise IncorrectPasswordException("Incorrect password")

        access_token = await token_service.create_token(
            token_type=TokenTypesEnum.access,
            user_id=user.id,
        )

        refresh_token = await token_service.create_token(
            token_type=TokenTypesEnum.refresh,
            user_id=user.id,
        )

        return access_token, refresh_token

    async def reset_password(
        self,
        token: str,
        new_password: str,
        token_service: StatefulTokenService,
        repo: UsersDAO,
    ) -> bool:
        """
        Метод сброса пароля пользователя.
        """
        token_data = await token_service.get_reset_token_data(token=token)

        if not token_data:
            raise InvalidTokenException("Invalid token")

        if token_data.used:
            raise InvalidTokenException("Token is already used")

        if token_data.expires_at < datetime.now(timezone.utc):
            raise TokenExpiredException("Token has expired")

        hashed_password = hash_helper.hash(plain_str=new_password)
        result = await repo.set_password(user_id=token_data.user_id, hashed_password=hashed_password)
        await token_service.mark_token_as_used(token_obj=token_data)

        return result

    # TODO: доделать после реализации notification service
    async def forgot_password(
        self,
        user_email: str,
        repo: UsersDAO,
        token_service: StatefulTokenService,
    ) -> str:
        """
        Метод генерации токена сброса пароля и инициации его отправки на email через notification_service.
        """

        user = await repo.get_user_by_email(email=user_email)

        if user:
            token = await token_service.create_stateful_token(user_id=user.id)

            # Интеграция с notification_service (пока заглушка)
            # reset_url = f"https://frontend.example.com/reset-password?token={token}"
            #
            # отправка через раббит в notification service

            return token

    async def logout_user(
        self,
        refresh_token: str,
        response: Response,
        token_service: JWTTokensService,
    ) -> bool:
        """
        Метод завершения сессии/выхода пользователя.
        """

        if not refresh_token:
            raise InvalidTokenException("Invalid token")

        await token_service.revoke_token(token=refresh_token)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return True

    async def authorize_user(
        self,
        token: str,
        token_service: JWTTokensService,
        repo: UsersDAO,
        permission: PermissionEnum,
    ) -> None:
        """
        Метод для авторизации пользователя.
        """
        token_payload = await token_service.validate_token(
            token=token,
            token_type=TokenTypesEnum.access,
        )
        user_id = token_payload.get("user_id")
        user = await repo.get_by_id(id=user_id)
        if not user or not user.is_active:
            raise UserNotFoundException("User not found")
        if not has_permission(role=user.role, permission=permission):
            raise PermissionDeniedException("Not enough permissions")
