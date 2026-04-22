from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, Params

from src.schemas.custom_positions_schemas import (
    CustomPositionCreateSchema,
    CustomPositionUpdateSchema,
    CustomPositionWithPermissionsReadSchema,
)
from src.schemas.enums import PositionSourceEnum
from src.schemas.system_positions_schemas import (
    PositionReadSchema,
)
from src.services.position_service import PositionService
from src.utils.dependencies import (
    get_position_service,
)

positions_router = APIRouter(prefix="/positions", tags=["Positions"])


@positions_router.get("", response_model=Page[PositionReadSchema])
async def get_positions(
    owner_id: int | None = None,
    position_source: PositionSourceEnum = Query(...),
    position_service: PositionService = Depends(get_position_service),
    page_params: Params = Depends(),
) -> Page[PositionReadSchema]:
    """Ручка для получения должностей"""

    return await position_service.get_positions(
        params=page_params,
        position_source=position_source,
        owner_id=owner_id,
    )


@positions_router.get("/{position_id}")
async def get_position(
    position_id: int,
    position_source: PositionSourceEnum = Query(...),
    position_service: PositionService = Depends(get_position_service),
) -> PositionReadSchema:
    """Ручка для получения одной должности"""

    return await position_service.get_position(
        position_id=position_id,
        position_source=position_source,
    )


@positions_router.post("", response_model=PositionReadSchema)
async def create_custom_position(
    data: CustomPositionCreateSchema,
    position_service: PositionService = Depends(get_position_service),
) -> PositionReadSchema:
    """Ручка для создания кастомной должности"""

    return await position_service.create_position(data=data)


@positions_router.patch("/{position_id}", response_model=CustomPositionWithPermissionsReadSchema)
async def update_custom_position(
    position_id: int,
    data: CustomPositionUpdateSchema,
    position_service: PositionService = Depends(get_position_service),
) -> CustomPositionWithPermissionsReadSchema:
    """Ручка для обновления кастомной должности"""

    return await position_service.update_position(
        position_id=position_id,
        data=data,
    )


@positions_router.delete("/{position_id}", status_code=204)
async def delete_custom_position(
    position_id: int,
    position_service: PositionService = Depends(get_position_service),
) -> None:
    """Ручка для удаления кастомной должности"""

    return await position_service.delete_position(position_id=position_id)
