from fastapi import APIRouter, Depends

from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import UserRead
from src.services.user_service import UserService
from src.utils.dependencies import get_user_service, get_users_dao

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/{user_id}/set-role-owner", response_model=UserRead)
async def set_role_owner(
        user_id: int,
        user_service: UserService = Depends(get_user_service),  # noqa: B008
        repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """
    Обновляет роль конкретного юзера с test_owner → owner.
    Обычно вызывается после успешной оплаты (например из webhook платёжки).
    """

    result = await user_service.set_role_owner(user_id, repo)
    return result
