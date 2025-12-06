from fastapi_pagination import Page, Params

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.usersDAO import UsersDAO
from src.models.users.users import Users
from src.schemas.permissions_schemas import PermissionReadSchema
from src.schemas.tokens_schemas import TokenTypesEnum
from src.schemas.users_schemas import (
    SubscriptionEnum,
    UserAuthRequestSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from src.services.token_service import JWTTokensService
from src.utils.exceptions import PermissionDeniedException, UserNotFoundException
from src.utils.logger_settings import logger


class UserService:
    """
    Класс сервиса для работы с пользователями.
    """

    def __init__(self, db_helper):
        self.db_helper = db_helper

    async def set_paid_owner(self, user_id: int, repo: UsersDAO) -> UserReadSchema:
        """
        Метод для обновления подписки с test на paid.
        """

        user = await repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")

        if user.subscription != SubscriptionEnum.test:
            logger.error(
                "Пользователю не удалось поменять подписку, т.к у него нет роли owner!",
                user_id=user.id,
            )

            raise PermissionDeniedException("User is not owner")

        updated_user = await repo.update(id=user_id, subscription=SubscriptionEnum.paid)

        logger.info(
            "Пользователю успешно поменяна подписка!",
            user_id=user.id,
        )

        return UserReadSchema.model_validate(updated_user)

    async def get_user_by_id(self, user_id: int, repo: UsersDAO) -> UserReadSchema:
        """Получает юзера по id"""

        user = await repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")

        return UserReadSchema.model_validate(user)

    async def get_users(self, repo: UsersDAO, params: Params) -> Page[Users]:
        """Получает всех юзеров"""

        users = await repo.get_users(params=params)

        if users.total == 0:
            raise UserNotFoundException("Users not found")

        return users

    async def update_user(
        self,
        token: UserAuthRequestSchema,
        token_service: JWTTokensService,
        user: UserUpdateSchema,
        repo: UsersDAO,
    ) -> UserReadSchema:
        """Обновляет данные пользователя"""

        token_payload = await token_service.validate_token(
            token.access_token,
            TokenTypesEnum.access,
        )

        prev_user = await repo.get_by_id(user.id)
        if not prev_user:
            raise UserNotFoundException("User not found")

        current_user_id = token_payload.get("user_id")
        if current_user_id != user.id:
            raise PermissionDeniedException("You can update just yours data")

        updated_user = await repo.update(
            prev_user.id,
            email=user.email,
        )

        logger.info(
            "Информация о пользователе id={user_id} успешно обновлена!",
            user_id=user.id,
        )
        return updated_user

    async def delete_user(self, user_id: int, repo: UsersDAO):
        """Удаляет пользователя по id"""

        user = await repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")

        logger.info(
            "Пользователь id={user_id} успешно удален!",
            user_id=user.id,
        )

        await repo.delete(user.id)

    async def set_user_permissions(
        self,
        user_id: int,
        permission_ids: list[int],
        user_repo: UsersDAO,
        perm_repo: PermissionsDAO,
    ) -> list[PermissionReadSchema]:
        """Обновляет список прав пользователя"""

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                await user_repo.update_user_permissions(
                    session=session,
                    user_id=user_id,
                    new_permission_ids=permission_ids,
                )

                permissions = await perm_repo.get_user_permissions_without_pagination(
                    session=session,
                    user_id=user_id,
                )

                return [PermissionReadSchema.model_validate(p) for p in permissions]
