from fastapi import APIRouter
from fastapi.params import Depends, Query
from fastapi_pagination import Page, Params

from src.schemas.enums import PositionSourceEnum
from src.schemas.permissions_schemas import PermissionReadSchema
from src.services.permission_service import PermissionService
from src.utils.dependencies import get_permissions_service

permissions_router = APIRouter(prefix="/permissions", tags=["Permissions"])


@permissions_router.get("/")
async def get_permissions(
    position_id: int | None = Query(None, description="ID должности"),
    user_id: int | None = Query(None, description="ID пользователя"),
    position_source: PositionSourceEnum | None = Query(None, description="Тип прав"),
    permissions_service: PermissionService = Depends(get_permissions_service),
    params: Params = Depends(),
) -> Page[PermissionReadSchema]:
    """
    Ручка для получения всех прав доступа
    с фильтрацией по position_id или user_id
    """

    return await permissions_service.get_permissions_filtered(
        position_id=position_id,
        position_source=position_source,
        user_id=user_id,
        params=params,
    )
