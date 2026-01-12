from datetime import datetime, timezone

from fastapi import Response
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from src.core.security.hash_helper import hash_helper
from src.dao.custom_positionsDAO import CustomPositionDAO
from src.dao.permissionsDAO import PermissionsDAO
from src.dao.system_positionsDAO import SystemPositionDAO
from src.dao.usersDAO import UsersDAO
from src.schemas.enums import PositionSourceEnum
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

    def __init__(
        self,
        db_helper,
        custom_repo: CustomPositionDAO,
        system_repo: SystemPositionDAO,
        user_repo: UsersDAO,
        permission_repo: PermissionsDAO,
    ):
        self.db_helper = db_helper
        self.custom_repo = custom_repo
        self.system_repo = system_repo
        self.user_repo = user_repo
        self.permission_repo = permission_repo

    async def register_user(
        self,
        data: UserRegisterSchema,
        token_service: JWTTokensService | None = None,
    ) -> UserReadSchema:
        """
        Метод регистрации пользователя.
        """

        existing_user = await self.user_repo.get_user_by_email(email=data.email)
        if existing_user:
            raise UserAlreadyExistsException("Данный пользователь уже существует.")

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
            owner_id = register_token_payload.get("owner_id")
            owner = await self.user_repo.get_by_id(id=owner_id)
            if not owner:
                raise UserNotFoundException(f"Владелец с user_id={owner_id} не найден")

            position_id = register_token_payload.get("position_id")
            position_source = register_token_payload.get("position_source")

            if position_id and position_source:
                if position_source == "system":
                    perm_ids = await self.permission_repo.get_permissions_ids_by_system_position(position_id=position_id)
                elif position_source == "custom":
                    perm_ids = await self.permission_repo.get_permissions_ids_by_custom_position(position_id=position_id)
                else:
                    raise PositionNotFoundException("Не определен position source для нахождения прав доступа.")
            else:
                perm_ids = []
        else:
            perm_ids = await self.permission_repo.get_owner_permissions_ids()

        if not perm_ids:
            raise PermissionsNotFound("Никаких прав доступа для этой должности не найдено.")

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                try:
                    user = await self.user_repo.create_user(
                        payload=payload,
                        session=session,
                    )

                except IntegrityError as e:
                    raise UserAlreadyExistsException("Данный пользователь уже существует.") from e

                if perm_ids:
                    await self.user_repo.assign_permissions(
                        user_id=user.id,
                        permissions=perm_ids,
                        session=session,
                    )

                result = UserReadSchema.model_validate(user)

        return result

    async def login_user(
        self,
        credentials: UserLoginSchema,
        token_service: JWTTokensService,
    ) -> tuple[str, str]:
        """
        Метод аутентификации пользователя.
        """
        user = await self.user_repo.get_user_by_email(email=credentials.email)
        if not user:
            raise UserNotFoundException("Пользователь не найден.")

        if not hash_helper.verify_password(plain_password=credentials.password, hashed_password=user.hashed_password):
            raise IncorrectPasswordException("Неверный пароль.")

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
    ) -> bool:
        """
        Метод сброса пароля пользователя.
        """
        token_data = await token_service.get_reset_token_data(token=token)

        if not token_data:
            raise InvalidTokenException("Невалидный токен.")

        if token_data.used:
            raise InvalidTokenException("Токен уже использован.")

        if token_data.expires_at < datetime.now(timezone.utc):
            raise TokenExpiredException("Токен уже просрочен.")

        hashed_password = hash_helper.hash(plain_str=new_password)
        result = await self.user_repo.set_password(user_id=token_data.user_id, hashed_password=hashed_password)
        await token_service.mark_token_as_used(token_obj=token_data)

        return result

    # TODO: доделать после реализации notification service
    async def forgot_password(
        self,
        user_email: EmailStr,
        token_service: StatefulTokenService,
    ) -> str:
        """
        Метод генерации токена сброса пароля и инициации его отправки на email через notification_service.
        """

        user = await self.user_repo.get_user_by_email(email=user_email)

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
            raise InvalidTokenException("Невалидный токен.")

        await token_service.revoke_token(token=refresh_token)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return True

    async def generate_register_token(
        self,
        employee_data: UserRegisterEmployeeSchema,
        token_service: JWTTokensService,
    ) -> dict:
        """Метод генерации инвайт токена."""

        owner_id = employee_data.owner_id
        owner = await self.user_repo.get_by_id(id=owner_id)
        if not owner:
            raise UserNotFoundException(f"Владелец с user_id={owner_id} не найден")

        if employee_data.position_source == PositionSourceEnum.system:
            position = await self.system_repo.get_by_id(id=employee_data.position_id)
        elif employee_data.position_source == PositionSourceEnum.custom:
            position = await self.custom_repo.get_by_id(id=employee_data.position_id)
        if not position:
            raise PositionNotFoundException("Должность не найдена.")

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
        required_permission: str,
        token_service: JWTTokensService,
    ) -> None:
        """
        Метод для авторизации пользователя.
        """
        token_payload = await token_service.validate_token(
            token=token,
            token_type=TokenTypesEnum.access,
        )
        user_id = token_payload.get("user_id")

        user = await self.user_repo.get_by_id(id=user_id)

        if not user or user.is_active is False:
            raise UserNotFoundException("Пользователь не найден или неактивен.")

        async with self.db_helper.async_session_maker() as session:
            permissions_objs = await self.permission_repo.get_user_permissions_without_pagination(
                user_id=user_id,
                session=session,
            )

            if not permissions_objs:
                raise PermissionDeniedException("Недостаточно прав.")

        user_permission_codes = {p.code_name for p in permissions_objs}

        if required_permission not in user_permission_codes:
            raise PermissionDeniedException(f"Нет обязательного права доступа: {required_permission}")
