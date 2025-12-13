from datetime import datetime, timezone

from fastapi import Response
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from src.core.security.hash_helper import hash_helper
from src.core.security.permissions import PermissionEnum, has_permission
from src.dao.permissionsDAO import PermissionsDAO
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
    PermissionsNotFound,
    PositionNotFoundException,
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
        token_service: JWTTokensService | None = None,
    ) -> UserReadSchema:
        """
        Метод регистрации пользователя.
        """

        existing_user = await user_repo.get_user_by_email(email=data.email)
        if existing_user:
            raise UserAlreadyExistsException("Данный пользователь уже существует.")

        hashed_password = hash_helper.hash(plain_str=data.password)
        payload = {
            "email": data.email,
            "hashed_password": hashed_password,
        }

        # TODO: переделать под должности, исправить
        if data.register_token:
            register_token_payload = await token_service.validate_token(
                token=data.register_token,
                token_type=TokenTypesEnum.register,
            )
            owner_id = register_token_payload.get("owner_id")
            owner = await user_repo.get_by_id(id=owner_id)
            if not owner:
                raise UserNotFoundException(f"Владелец с user_id={owner_id} не найден")

            position_id = register_token_payload.get("position_id")
            position_source = register_token_payload.get("position_source")
        else:
            position_id = data.position_id
            position_source = data.position_source

        if position_id and position_source:
            if position_source == "system":
                perm_ids = await perm_repo.get_permissions_ids_by_system_position(position_id=position_id)
            elif position_source == "custom":
                perm_ids = await perm_repo.get_permissions_ids_by_custom_position(position_id=position_id)
            else:
                raise PositionNotFoundException("Не определен position source для нахождения прав доступа.")
        else:
            perm_ids = []

        if not perm_ids:
            raise PermissionsNotFound("Никаких прав доступа для этой должности не найдено.")

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                try:
                    user = await user_repo.create_user(
                        payload=payload,
                        session=session,
                    )

                except IntegrityError as e:
                    raise UserAlreadyExistsException("User already exists") from e

                if perm_ids:
                    await user_repo.assign_permissions(
                        user_id=user.id,
                        permissions=perm_ids,
                        session=session,
                    )

                result = UserReadSchema.model_validate(user)

        return result

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
        user_email: EmailStr,
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
        owner_id = employee_data.owner_id
        owner = await repo.get_by_id(id=owner_id)
        if not owner:
            raise UserNotFoundException(f"Владелец с user_id={owner_id} не найден")

        register_token = await token_service.create_register_token(
            token_type=TokenTypesEnum.register,
            pvz_id=employee_data.pvz_id,
            owner_id=employee_data.owner_id,
            position_id=employee_data.position_id,
            position_source=employee_data.position_source,
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
