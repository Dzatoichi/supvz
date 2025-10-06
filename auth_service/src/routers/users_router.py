from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.core.security.permissions import PermissionEnum
from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import UserAuthRequestSchema, UserReadSchema, UserUpdateSchema
from src.services.auth_service import AuthService
from src.services.token_service import JWTTokensService
from src.services.user_service import UserService
from src.utils.dependencies import (
    get_access_token_from_cookie,
    get_auth_service,
    get_jwt_tokens_service,
    get_user_service,
    get_users_dao,
)
from src.utils.rate_limiter import limiter

users_router = APIRouter(prefix="/users", tags=["users"])


@limiter.limit("5/minute")
@users_router.post("/{user_id}/set-role-owner", response_model=UserReadSchema)
async def set_role_owner(
    request: Request,
    user_id: int,
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """
    Ручка обновления роли юзера с test_owner → owner.
    Обычно вызывается после успешной оплаты (например из webhook платёжки).
    """

    result = await user_service.set_role_owner(user_id=user_id, repo=repo)
    return result


@users_router.get("/{user_id}", response_model=UserReadSchema)
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


@users_router.get("", response_model=list[UserReadSchema])
async def get_users(
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """Получает список данных о каждом юзере"""

    result = await user_service.get_users(repo=repo)
    return result


@users_router.patch("", response_model=UserUpdateSchema)
async def update_user(
    user: UserUpdateSchema,
    access_token: str = Depends(get_access_token_from_cookie),  # noqa: B008
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
):
    """Заменяет имя и номер телефона существующего пользователя"""

    token = UserAuthRequestSchema(access_token=access_token)
    result = await user_service.update_user(token=token, token_service=token_service, user=user, repo=repo)
    return result


@users_router.delete("/{user_id}", response_model=UserReadSchema)
async def delete_user(
    user_id: int,
    access_token: str = Depends(get_access_token_from_cookie),  # noqa: B008
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    user_service: UserService = Depends(get_user_service),  # noqa: B008
    repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),  # noqa: B008
):
    """Удаление пользователя по id (только с правом DELETE_EMPLOYEES)"""

    # Используем зависимость get_access_token_from_cookie
    auth_request = UserAuthRequestSchema(access_token=access_token)

    # Используем авторизацию
    role, permissions = await auth_service.authorize_user(auth_request, token_service, repo)

    # Проверяем наличие права на удаление сотрудников
    if PermissionEnum.DELETE_EMPLOYEES not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для удаления пользователей"
        )

    result = await user_service.delete_user(user_id=user_id, repo=repo)
    return result
