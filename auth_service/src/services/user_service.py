from fastapi import HTTPException, status

from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import SubscriptionEnum, UserReadSchema, UserRole
from src.utils.logger_settings import logger

from auth_service.src.schemas.tokens_schemas import TokenTypesEnum
from auth_service.src.services.token_service import JWTTokensService


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

        if user.role != UserRole.owner:
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

        return UserReadSchema(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
            role=updated_user.role,
            subscription=updated_user.subscription,
            created_at=updated_user.created_at,
        )

    async def get_current_user(
        self,
        access_token: str,
        repo: UsersDAO,
        token_service: JWTTokensService,
    ) -> UserReadSchema:
        payload = token_service.validate_token(
            token=access_token,
            token_type=TokenTypesEnum.access)
        user = repo.get_by_id(payload["id"])


