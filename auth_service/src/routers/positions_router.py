from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.positionsDAO import PositionDAO
from src.schemas.perm_positions_schemas import PositionCreateSchema, PositionReadSchema, PositionUpdateSchema
from src.services.position_service import PositionService
from src.utils.dependencies import (
    get_permissions_dao,
    get_position_dao,
    get_position_service,
)

positions_router = APIRouter(prefix="/positions", tags=["Position"])


@positions_router.get("/")
async def get_positions(
    owner_id: int | None = None,
    position_service: PositionService = Depends(get_position_service),
    repo: PositionDAO = Depends(get_position_dao),
    page_params: Params = Depends(),
) -> Page[PositionReadSchema]:
    """Ручка для получения должностей"""

    return await position_service.get_positions(repo=repo, params=page_params, owner_id=owner_id)


@positions_router.get("/{position_id}")
async def get_position(
    position_id: int,
    position_service: PositionService = Depends(get_position_service),
    repo: PositionDAO = Depends(get_position_dao),
) -> PositionReadSchema:
    """Ручка для получения одной должности"""

    return await position_service.get_position(
        position_id=position_id,
        repo=repo,
    )


@positions_router.post("/", response_model=PositionReadSchema)
async def create_position(
    data: PositionCreateSchema,
    position_service: PositionService = Depends(get_position_service),
    repo: PositionDAO = Depends(get_position_dao),
    permission_repo: PermissionsDAO = Depends(get_permissions_dao),
) -> PositionReadSchema:
    """Ручка для создания должности"""

    position = await position_service.create_position(
        data=data,
        position_repo=repo,
        permission_repo=permission_repo,
    )

    return PositionReadSchema.model_validate(position)


@positions_router.patch("/{position_id}", response_model=PositionReadSchema)
async def update_position(
    position_id: int,
    data: PositionUpdateSchema,
    position_service: PositionService = Depends(get_position_service),
    position_repo: PositionDAO = Depends(get_position_dao),
    permission_repo: PermissionsDAO = Depends(get_permissions_dao),
) -> PositionReadSchema:
    """Ручка для обновления должности"""

    return await position_service.update_position(
        position_id=position_id,
        data=data,
        position_repo=position_repo,
        permission_repo=permission_repo,
    )


@positions_router.delete("/{position_id}", status_code=204)
async def delete_position(
    position_id: int,
    position_service: PositionService = Depends(get_position_service),
    repo: PositionDAO = Depends(get_position_dao),
) -> None:
    """Ручка для удаления должности"""

    return await position_service.delete_position(
        position_id=position_id,
        repo=repo,
    )
