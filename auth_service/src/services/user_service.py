from fastapi import HTTPException, status

from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import UserReadSchema, UserRole


class UserService:
    """
    Класс сервиса для работы с пользователями.
    """

    async def set_role_owner(self, user_id: int, repo: UsersDAO) -> UserReadSchema:
        """
        Метод обновления роли пользователя с test_owner → owner.
        """

        user = await repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")

        if user.role != UserRole.test_owner:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "User is not test_owner",
            )

        updated_user = await repo.update(user_id, role=UserRole.owner)

        return UserReadSchema(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
            role=updated_user.role,
            created_at=updated_user.created_at,
        )
