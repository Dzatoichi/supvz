from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from src.schemas.positions_schemas import (
    PositionCreateSchema,
    PositionReadSchema,
    PositionUpdateSchema,
    PositionWithPermissionsReadSchema,
)
from src.services.position_service import PositionService
from src.utils.dependencies import (
    get_position_service,
)

positions_router = APIRouter(prefix="/positions", tags=["Position"])


@positions_router.get("/", response_model=Page[PositionReadSchema])
async def get_positions(
    owner_id: int | None = None,
    position_service: PositionService = Depends(get_position_service),
    page_params: Params = Depends(),
) -> Page[PositionReadSchema]:
    """Ручка для получения должностей"""

    return await position_service.get_positions(
        params=page_params,
        owner_id=owner_id,
    )


@positions_router.get("/{position_id}")
async def get_position(
    position_id: int,
    position_service: PositionService = Depends(get_position_service),
) -> PositionReadSchema:
    """Ручка для получения одной должности"""

    return await position_service.get_position(position_id=position_id)


@positions_router.post("/", response_model=PositionReadSchema)
async def create_position(
    data: PositionCreateSchema,
    position_service: PositionService = Depends(get_position_service),
) -> PositionReadSchema:
    """Ручка для создания должности"""

    position = await position_service.create_position(data=data)

    return PositionReadSchema.model_validate(position)


@positions_router.patch("/{position_id}", response_model=PositionWithPermissionsReadSchema)
async def update_position(
    position_id: int,
    data: PositionUpdateSchema,
    position_service: PositionService = Depends(get_position_service),
) -> PositionWithPermissionsReadSchema:
    """Ручка для обновления должности"""

    return await position_service.update_position(
        position_id=position_id,
        data=data,
    )


@positions_router.delete("/{position_id}", status_code=204)
async def delete_position(
    position_id: int,
    position_service: PositionService = Depends(get_position_service),
) -> None:
    """Ручка для удаления должности"""

    return await position_service.delete_position(position_id=position_id)
