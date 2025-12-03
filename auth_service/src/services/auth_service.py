from datetime import datetime, timezone

from fastapi import Response

from src.core.security.hash_helper import hash_helper
from src.core.security.permissions import PermissionEnum, has_permission
from src.dao.usersDAO import UsersDAO
from src.schemas.tokens_schemas import TokenTypesEnum
from src.schemas.users_schemas import (
    UserLoginSchema,
    UserReadSchema,
    UserRegisterEmployeeSchema,
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

    async def register_user(
        self,
        data: UserRegisterSchema,
        repo: UsersDAO,
        token_service: JWTTokensService | None = None,
    ) -> UserReadSchema:
        """
        Метод регистрации пользователя.
        """
        user = await repo.get_user_by_email(email=data.email)
        if user:
            raise UserAlreadyExistsException("User already exists")

        hashed_password = hash_helper.hash(plain_str=data.password)
        payload = {
            "email": data.email,
            "hashed_password": hashed_password,
        }

        if data.register_token:
            register_token_payload = await token_service.validate_token(
                token=data.register_token,
                token_type=TokenTypesEnum.register,
            )

            owner = repo.get_by_id(register_token_payload.get("owner_id"))
            if not owner:
                raise UserNotFoundException("Referenced owner_id not found")

            payload["role"] = register_token_payload.get("role")

        return await repo.create(payload=payload)

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

    async def generate_register_token(
        self,
        employee_data: UserRegisterEmployeeSchema,
        token_service: JWTTokensService,
        repo: UsersDAO,
    ) -> dict:
        owner = await repo.get_by_id(employee_data.owner_id)
        if not owner:
            raise UserNotFoundException("Пользователь не найден")

        register_token = await token_service.create_register_token(
            token_type=TokenTypesEnum.register,
            pvz_id=employee_data.pvz_id,
            owner_id=employee_data.owner_id,
            role=employee_data.role,
        )
        return {"register_token": register_token}

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
