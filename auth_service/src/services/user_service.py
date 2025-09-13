from fastapi import HTTPException, status

from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import UserRead, UserRole


class UserService:
    
    async def set_role_owner(self, user_id: int, repo: UsersDAO) -> UserRead:
        """Обновляет роль конкретного юзера с test_owner → owner."""

        user = await repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        if user.role != UserRole.test_owner:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "User is not test_owner",
            )

        updated_user = await repo.update(user_id, role=UserRole.owner)

        return UserRead(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
            role=updated_user.role,
            created_at=updated_user.created_at,
        )
