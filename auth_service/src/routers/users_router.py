from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from src.dao.tokensDAO import RefreshTokensDAO
from src.dao.usersDAO import UsersDAO
from src.schemas.users_schemas import (
    UserAuthRequestSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from src.services.token_service import JWTTokensService
from src.services.user_service import UserService
from src.utils.dependencies import (
    get_access_token_from_cookie,
    get_jwt_tokens_service,
    get_refresh_token_dao,
    get_user_service,
    get_users_dao,
)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/{user_id}/set_paid_sub", response_model=UserReadSchema)
async def set_paid_sub(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    repo: UsersDAO = Depends(get_users_dao),
) -> UserReadSchema:
    """
    Ручка обновления подписки владельца с test → paid.
    Обычно вызывается после успешной оплаты.
    """

    result = await user_service.set_paid_owner(user_id=user_id, repo=repo)
    return result


@users_router.get("/{user_id}", response_model=UserReadSchema)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    repo: UsersDAO = Depends(get_users_dao),
) -> UserReadSchema:
    """
    Получает все данные о юзере по id
    """

    result = await user_service.get_user_by_id(user_id=user_id, repo=repo)
    return result


@users_router.get("", response_model=Page[UserReadSchema])
async def get_users(
    user_service: UserService = Depends(get_user_service),
    repo: UsersDAO = Depends(get_users_dao),
    params: Params = Depends(),
) -> Page[UserReadSchema]:
    """
    Получает список данных о каждом юзере
    """

    result = await user_service.get_users(repo=repo, params=params)
    return result


@users_router.patch("/me", response_model=UserReadSchema)
async def update_user(
    user: UserUpdateSchema,
    access_token: str = Depends(get_access_token_from_cookie),
    user_service: UserService = Depends(get_user_service),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
    repo: UsersDAO = Depends(get_users_dao),
    refresh_repo: RefreshTokensDAO = Depends(get_refresh_token_dao),
) -> UserReadSchema:
    """
    Ручка для обновления пользователя.
    """

    token = UserAuthRequestSchema(access_token=access_token)
    result = await user_service.update_user(
        token=token,
        token_service=token_service,
        user=user,
        repo=repo,
        refresh_repo=refresh_repo,
    )
    return result


@users_router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    repo: UsersDAO = Depends(get_users_dao),
) -> None:
    """
    Удаление пользователя по id
    """
    await user_service.delete_user(user_id=user_id, repo=repo)


@users_router.get("/me", response_model=UserReadSchema)
async def get_сurrent_user(
    access_token: str = Depends(get_access_token_from_cookie),
    user_service: UserService = Depends(get_user_service),
    repo: UsersDAO = Depends(get_users_dao),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
):
    """Получение всех данных пользователя по access token"""

    token = UserAuthRequestSchema(access_token=access_token)
    result = await user_service.get_current_user(token=token, token_service=token_service, repo=repo)
    return result
