from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.schemas.shifts_schemas import (
    ShiftCreateSchema,
    ShiftFilterSchema,
    ShiftReadSchema,
    ShiftUpdateSchema,
)
from src.services.shift_service import ShiftService
from src.utils.dependencies import get_shift_service

shifts_router = APIRouter(prefix="/shifts", tags=["Shifts"])


@shifts_router.post("", response_model=ShiftReadSchema, status_code=status.HTTP_201_CREATED)
async def create_shift(
    data: ShiftCreateSchema,
    service: ShiftService = Depends(get_shift_service),
) -> ShiftReadSchema:
    return await service.create_shift(data)


@shifts_router.get("/{shift_id}", response_model=ShiftReadSchema)
async def get_shift(
    shift_id: int,
    service: ShiftService = Depends(get_shift_service),
) -> ShiftReadSchema:
    return await service.get_shift_by_id(shift_id)


@shifts_router.get("", response_model=Page[ShiftReadSchema])
async def get_shifts(
    params: Params = Depends(),
    scheduled_shift_id: int | None = Query(None),
    started_at_from: datetime | None = Query(None),
    started_at_to: datetime | None = Query(None),
    ended_at_from: datetime | None = Query(None),
    ended_at_to: datetime | None = Query(None),
    is_active: bool | None = Query(None),
    service: ShiftService = Depends(get_shift_service),
) -> Page[ShiftReadSchema]:
    filters = ShiftFilterSchema(
        scheduled_shift_id=scheduled_shift_id,
        started_at_from=started_at_from,
        started_at_to=started_at_to,
        ended_at_from=ended_at_from,
        ended_at_to=ended_at_to,
        is_active=is_active,
    )
    return await service.get_shifts(params=params, filters=filters)


@shifts_router.patch("/{shift_id}", response_model=ShiftReadSchema)
async def update_shift(
    shift_id: int,
    data: ShiftUpdateSchema,
    service: ShiftService = Depends(get_shift_service),
) -> ShiftReadSchema:
    return await service.update_shift(shift_id, data)


@shifts_router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shift(
    shift_id: int,
    service: ShiftService = Depends(get_shift_service),
) -> None:
    await service.delete_shift(shift_id)
