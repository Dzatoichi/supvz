from fastapi_pagination import Page, Params, paginate

from src.dao.usersDAO import UsersDAO
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

    async def get_users(self, repo: UsersDAO, params: Params) -> Page[UserReadSchema]:
        """Получает всех юзеров"""

        users = await repo.get_all()

        users_page = paginate(users, params)

        users_page.items = [UserReadSchema.model_validate(user) for user in users_page.items]

        return users_page

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
