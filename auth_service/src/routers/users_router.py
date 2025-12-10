from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.usersDAO import UsersDAO
from src.schemas.permissions_schemas import PermissionReadSchema
from src.schemas.users_schemas import (
    StatusResponseSchema,
    UpdateUserPermissionsSchema,
    UpdateUsersPermissionsSchema,
    UserAuthRequestSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from src.services.token_service import JWTTokensService
from src.services.user_service import UserService
from src.utils.dependencies import (
    get_access_token_from_cookie,
    get_jwt_tokens_service,
    get_permissions_dao,
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


@users_router.patch("", response_model=UserReadSchema)
async def update_user(
    user: UserUpdateSchema,
    access_token: str = Depends(get_access_token_from_cookie),
    user_service: UserService = Depends(get_user_service),
    token_service: JWTTokensService = Depends(get_jwt_tokens_service),
    repo: UsersDAO = Depends(get_users_dao),
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
    )
    return result


@users_router.put("/{user_id}/permissions", status_code=200)
async def update_permissions(
    user_id: int,
    data: UpdateUserPermissionsSchema,
    user_service: UserService = Depends(get_user_service),
    user_repo: UsersDAO = Depends(get_users_dao),
    perm_repo: PermissionsDAO = Depends(get_permissions_dao),
) -> list[PermissionReadSchema]:
    """
    Полностью перезаписывает права пользователя.
    """

    return await user_service.set_user_permissions(
        user_id=user_id,
        permission_ids=data.permission_ids,
        user_repo=user_repo,
        perm_repo=perm_repo,
    )


@users_router.put("/permissions/", response_model=StatusResponseSchema)
async def update_users_permissions(
    data: UpdateUsersPermissionsSchema,
    user_service: UserService = Depends(get_user_service),
    repo: UsersDAO = Depends(get_users_dao),
) -> StatusResponseSchema:
    """
    Ручка для bulk update permissions у юзеров.
    Старые права удаляются, новые назначаются.
    """
    return await user_service.update_users_permissions(data=data, repo=repo)


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
