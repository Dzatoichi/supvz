from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.security.permissions import PermissionEnum
from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import UserAuthRequest, UserRead, UserUpdate
from src.services.auth_service import AuthService
from src.services.token_service import JWTTokensService
from src.services.user_service import UserService
from src.utils.dependencies import get_auth_service, get_jwt_tokens_service, get_user_service, get_users_dao

users_router = APIRouter(prefix="/users", tags=["users"])

security = HTTPBearer()


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
    credentials: HTTPAuthorizationCredentials = Depends(security),   # noqa: B008
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """Заменяет имя и номер телефона существующего пользователя"""

    token = UserAuthRequest(access_token=credentials.credentials)
    result = await user_service.update_user(token=token, token_service=token_service, user=user, repo=repo)
    return result


@users_router.post("/{user_id}/delete-user", response_model=UserRead)
async def delete_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),    # noqa: B008
    auth_service: AuthService = Depends(get_auth_service),   # noqa: B008
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),   # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),   # noqa: B008
):
    """Удаление пользователя по id (только с правом DELETE_EMPLOYEES)"""

    # Используем токен из credentials
    auth_request = UserAuthRequest(access_token=credentials.credentials)

    # Используем авторизацию
    role, permissions = await auth_service.authorize_user(auth_request, token_service, repo)

    # Проверяем наличие права на удаление сотрудников
    if PermissionEnum.DELETE_EMPLOYEES not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для удаления пользователей"
        )

    result = await user_service.delete_user(user_id=user_id, repo=repo)
    return result
