from fastapi import APIRouter, Depends

from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import UserRead, UserUpdate
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

    result = await user_service.set_role_owner(user_id=user_id, repo=repo)
    return result


@users_router.get("/{user_id}/get-user", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """
    Получает все данные о юзере по id
    """

    result = await user_service.get_user_by_id(user_id=user_id, repo=repo)
    return result


@users_router.get("/get-users", response_model=list[UserRead])
async def get_users(
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """Получает список данных о каждом юзере"""

    result = await user_service.get_users(repo=repo)
    return result


@users_router.post("/update-user", response_model=UserUpdate)
async def update_user(
    user: UserUpdate,
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """Заменяет имя и номер телефона существующего пользователя"""

    result = await user_service.update_user(user=user, repo=repo)
    return result


@users_router.post("/{user_id}/delete-user", response_model=UserRead)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """Удаление пользователя по id"""

    result = await user_service.delete_user(user_id=user_id, repo=repo)
    return result
