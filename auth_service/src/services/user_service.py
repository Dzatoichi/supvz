from fastapi import HTTPException, status

from src.core.security.permissions import get_permissions_for_role
from src.dao.usersDAO import UsersDAO
from src.schemas.tokens import TokenTypesEnum
from src.schemas.users_schemas import UserRead, UserRole, UserUpdate
from src.services.token_service import JWTTokensService


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
            permissions=get_permissions_for_role(updated_user.role),
            created_at=updated_user.created_at,
        )

    async def get_user_by_id(self, user_id: int, repo: UsersDAO) -> UserRead:
        """Получает юзера по id"""

        user = await repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        return UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            permissions=get_permissions_for_role(user.role),
            created_at=user.created_at,
        )

    async def get_users(self, repo: UsersDAO) -> list[UserRead]:
        """Получает всех юзеров"""

        users = await repo.get_all()

        return [
            UserRead(
                id=user.id,
                email=user.email,
                name=user.name,
                role=user.role,
                permissions=get_permissions_for_role(user.role),
                created_at=user.created_at,
            )
            for user in users
        ]

    async def update_user(
        self,
        token: str,
        token_service: JWTTokensService,
        user: UserUpdate,
        repo: UsersDAO,
    ) -> UserUpdate:
        """Обновляет данные пользователя"""

        token_payload = await token_service.validate_token(
            token.access_token,
            TokenTypesEnum.access,
        )

        current_user_id = token_payload.get("user_id")

        # Проверяем, что пользователь обновляет свои данные
        if current_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Можно обновлять только свои данные")

        # Проверяем существование пользователя
        prev_user = await repo.get_by_id(user.id)
        if not prev_user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        # Обновляем данные
        upated_user = await repo.update(prev_user.id, name=user.name, phone_number=user.phone_number, email=user.email)
        return UserUpdate(
            id=upated_user.id,
            name=upated_user.name,
            phone_number=upated_user.phone_number,
            email=upated_user.email,
        )

    async def delete_user(self, user_id: int, repo: UsersDAO) -> UserRead:
        """Удаляет пользователя по id"""

        user = await repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        await repo.delete(user.id)
        return UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            permissions=get_permissions_for_role(user.role),
            created_at=user.created_at,
        )
