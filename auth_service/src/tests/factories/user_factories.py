import bcrypt
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_permissions.user_permissions import UserPermissions
from src.models.users.users import Users
from src.schemas.enums import PositionSourceEnum
from src.schemas.users_schemas import (
    PasswordResetConfirmSchema,
    SubscriptionEnum,
    UpdateUserPermissionsSchema,
    UpdateUsersPermissionsSchema,
    UserForgotPasswordSchema,
    UserLoginSchema,
    UserPermissionSchema,
    UserRegisterEmployeeSchema,
    UserRegisterSchema,
    UserUpdateSchema,
)
from src.tests.factories.base_factories import AsyncPersistenceFactory


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8"),
    )


DEFAULT_PASSWORD = "TestPassword123!"


class UserFactory(AsyncPersistenceFactory[UserRegisterSchema]):
    """
    Фабрика пользователя.

    - build() -> UserRegisterSchema (payload для POST /auth/register)
    - create_async() -> Users (создаёт в БД с хешированием пароля)

    Для тестов логина используй DEFAULT_PASSWORD или передай свой.
    """

    __model__ = UserRegisterSchema
    __model_cls__ = Users

    password = DEFAULT_PASSWORD
    confirm_password = DEFAULT_PASSWORD
    register_token = None
    position_id = 1
    position_source = PositionSourceEnum.system

    @classmethod
    async def create_async(cls, session: AsyncSession, **kwargs) -> Users:
        """
        Создаёт пользователя в БД.
        - Хеширует пароль
        - Игнорирует поля, которых нет в модели Users
        """
        data = cls.build(**kwargs)
        db_obj = Users(
            email=data.email,
            hashed_password=hash_password(data.password),
            is_active=True,
            is_deleted=False,
            subscription=SubscriptionEnum.test,
        )

        session.add(db_obj)
        await session.flush()
        return db_obj


class UserLoginFactory(AsyncPersistenceFactory[UserLoginSchema]):
    """
    Фабрика для payload логина.
    """

    __model__ = UserLoginSchema

    password = DEFAULT_PASSWORD


class ForgotPasswordFactory(AsyncPersistenceFactory[UserForgotPasswordSchema]):
    """
    Фабрика для payload POST /auth/forgot_password.
    """

    __model__ = UserForgotPasswordSchema


class ResetPasswordFactory(AsyncPersistenceFactory[PasswordResetConfirmSchema]):
    """
    Фабрика для payload POST /auth/reset_password.
    """

    __model__ = PasswordResetConfirmSchema

    token = Use(lambda: "mock_reset_token_12345")
    new_password = "NewSecurePassword456!"
    confirm_new_password = "NewSecurePassword456!"


class RegisterEmployeeFactory(AsyncPersistenceFactory[UserRegisterEmployeeSchema]):
    """
    Фабрика для payload POST /auth/generate_register_token.
    """

    __model__ = UserRegisterEmployeeSchema

    pvz_id = 1
    owner_id = 1
    position_id = 1
    position_source = PositionSourceEnum.system


class UserPermissionFactory(AsyncPersistenceFactory[UserPermissionSchema]):
    """
    Фабрика для связи пользователя с правом доступа.
    """

    __model__ = UserPermissionSchema
    __model_cls__ = UserPermissions

    user_id = 0
    permission_id = 0


class UserUpdatePayloadFactory(ModelFactory[UserUpdateSchema]):
    """
    Фабрика для PATCH /users/{user_id}
    Схема содержит только email.
    """

    __model__ = UserUpdateSchema


class UpdateUserPermissionsPayloadFactory(ModelFactory[UpdateUserPermissionsSchema]):
    """
    Фабрика для PUT /users/{user_id}/permissions
    """

    __model__ = UpdateUserPermissionsSchema

    permission_ids = Use(lambda: [])


class UpdateUsersPermissionsPayloadFactory(ModelFactory[UpdateUsersPermissionsSchema]):
    """
    Фабрика для PUT /users/permissions/ (bulk update)
    Структура: users - список ID юзеров, new_permission_ids - список ID прав
    """

    __model__ = UpdateUsersPermissionsSchema

    users = Use(lambda: [])
    new_permission_ids = Use(lambda: [])
