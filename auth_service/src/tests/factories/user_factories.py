import random

from polyfactory import Use
from polyfactory.decorators import post_generated
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security.hash_helper import hash_helper
from src.models.users.users import Users
from src.schemas.enums import PositionSourceEnum
from src.schemas.users_schemas import (
    PasswordResetConfirmSchema,
    UpdateUsersPermissionsSchema,
    UserLoginSchema,
    UserPasswordUpdateSchema,
    UserRegisterEmployeeSchema,
    UserRegisterSchema,
)
from src.tests.factories.base_factories import faker


class UserFactory:
    DEFAULT_PASSWORD = "Password123!"

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        *,
        email: str | None = None,
        password: str | None = None,
        is_active: bool = True,
    ):
        raw_password = password or cls.DEFAULT_PASSWORD

        user = Users(
            email=email or faker.email(),
            hashed_password=hash_helper.hash(raw_password),
            is_active=is_active,
        )

        session.add(user)
        await session.flush()
        return user


class UserRegisterPayloadFactory(ModelFactory[UserRegisterSchema]):
    __model__ = UserRegisterSchema

    email = Use(faker.email)
    password = "Password123!"
    position_source = PositionSourceEnum.system
    position_id = Use(faker.random_int, min=1, max=100)

    @post_generated
    @classmethod
    def confirm_password(cls, password: str, **_):
        return password


class UserLoginPayloadFactory(ModelFactory[UserLoginSchema]):
    """Фабрика для генерации тела запроса на логин"""

    __model__ = UserLoginSchema

    email = Use(faker.email)
    password = "Password123!"


class UserPasswordUpdatePayloadFactory(ModelFactory[UserPasswordUpdateSchema]):
    """Фабрика для смены пароля"""

    __model__ = UserPasswordUpdateSchema

    current_password = "Password123!"
    new_password = "NewPassword1!"
    confirm_password = "NewPassword1!"


class PasswordResetConfirmPayloadFactory(ModelFactory[PasswordResetConfirmSchema]):
    """Фабрика для подтверждения сброса пароля"""

    __model__ = PasswordResetConfirmSchema

    token = Use(faker.sha256)
    new_password = "NewPassword1!"
    confirm_new_password = "NewPassword1!"


class UpdateUsersPermissionsPayloadFactory(ModelFactory[UpdateUsersPermissionsSchema]):
    """Фабрика для массового обновления прав"""

    __model__ = UpdateUsersPermissionsSchema

    users = Use(lambda: [faker.random_int(min_value=1, max_value=1000) for _ in range(random.randint(1, 5))])

    new_permission_ids = Use(lambda: [faker.random_int(min_value=1, max_value=50) for _ in range(random.randint(1, 3))])


class UserRegisterEmployeePayloadFactory(ModelFactory[UserRegisterEmployeeSchema]):
    """Фабрика для регистрации сотрудника (генерация токена)"""

    __model__ = UserRegisterEmployeeSchema

    pvz_id = Use(faker.random_int, min_value=1, max_value=500)
    owner_id = Use(faker.random_int, min_value=1, max_value=500)
    position_id = Use(faker.random_int, min_value=1, max_value=100)
    position_source = PositionSourceEnum.system
