from fastapi import HTTPException, status
from fastapi_pagination import Page, Params, paginate

from src.dao.tokensDAO import RefreshTokensDAO
from src.dao.usersDAO import UsersDAO
from src.schemas.tokens_schemas import TokenTypesEnum
from src.schemas.users_schemas import (
    SubscriptionEnum,
    UserAuthRequestSchema,
    UserReadSchema,
    UserRoleEnum,
    UserUpdateSchema,
)
from src.services.token_service import JWTTokensService
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
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")

        if user.role != UserRoleEnum.owner:
            logger.error(
                "Пользователю не удалось поменять подписку, т.к у него нет роли owner!",
                user_id=user.id,
            )

            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "User is not owner",
            )

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
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

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
        refresh_repo: RefreshTokensDAO,
    ) -> UserReadSchema:
        """Обновляет данные пользователя"""

        token_payload = await token_service.validate_token(
            token.access_token,
            TokenTypesEnum.access,
        )
        user_id = token_payload.get("user_id")
        current_user = await repo.get_by_id(user_id)
        if not current_user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        updated_user = await repo.update(
            email=user.email,
        )
        logger.info(
            f"Информация о пользователе {updated_user.email} успешно обновлена!",
        )
        return updated_user

    async def delete_user(self, user_id: int, repo: UsersDAO):
        """Удаляет пользователя по id"""

        user = await repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        logger.info(
            "Пользователь id={user_id} успешно удален!",
            user_id=user.id,
        )

        await repo.delete(user.id)

    async def get_current_user(
        self,
        token: UserAuthRequestSchema,
        repo: UsersDAO,
        token_service: JWTTokensService,
    ) -> UserReadSchema:
        token_payload = token_service.validate_token(token=token.access_token, token_type=TokenTypesEnum.access)
        user_id = token_payload.get("user_id")
        user = repo.get_by_id(user_id)
        return UserReadSchema.model_validate(user)
