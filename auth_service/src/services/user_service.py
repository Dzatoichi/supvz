from fastapi import HTTPException, status

from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import SubEnum, UserReadSchema, UserRole
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

        if user.role != UserRole.owner:
            logger.error(
                "Пользователю не удалось поменять подписку, т.к у него нет роли owner!",
                user_id=user.id,
            )

            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "User is not owner",
            )

        updated_user = await repo.update(id=user_id, subscription=SubEnum.paid)

        logger.info(
            "Пользователю успешно поменяна подписка!",
            user_id=user.id,
        )

        return UserReadSchema(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
            role=updated_user.role,
            sub=updated_user.subscription,
            created_at=updated_user.created_at,
        )
