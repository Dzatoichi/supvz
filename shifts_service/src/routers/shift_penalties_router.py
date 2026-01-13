from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.schemas.shift_penalties_schemas import (
    PenaltyTypeEnum,
    ShiftPenaltyCreateSchema,
    ShiftPenaltyFilterSchema,
    ShiftPenaltyReadSchema,
    ShiftPenaltySummarySchema,
    ShiftPenaltyUpdateSchema,
)
from src.services.shift_penalties_service import ShiftPenaltiesService
from src.utils.dependencies import get_shift_penalties_service

shift_penalties_router = APIRouter(prefix="/shift-penalties", tags=["Shift Penalties"])


@shift_penalties_router.post(
    "",
    response_model=ShiftPenaltyReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_penalty(
    data: ShiftPenaltyCreateSchema,
    service: ShiftPenaltiesService = Depends(get_shift_penalties_service),
) -> ShiftPenaltyReadSchema:
    """Создать новый штраф для смены."""
    return await service.create_penalty(data)


@shift_penalties_router.get(
    "",
    response_model=Page[ShiftPenaltyReadSchema],
)
async def get_penalties(
    params: Params = Depends(),
    scheduled_shift_id: int | None = Query(None, description="ID запланированной смены"),
    penalty_type: PenaltyTypeEnum | None = Query(None, alias="type", description="Тип штрафа"),
    penalty_points_min: int | None = Query(None, ge=0, description="Минимальное количество баллов"),
    penalty_points_max: int | None = Query(None, ge=0, description="Максимальное количество баллов"),
    detected_at_from: datetime | None = Query(None, description="Дата обнаружения от"),
    detected_at_to: datetime | None = Query(None, description="Дата обнаружения до"),
    created_at_from: datetime | None = Query(None, description="Дата создания от"),
    created_at_to: datetime | None = Query(None, description="Дата создания до"),
    service: ShiftPenaltiesService = Depends(get_shift_penalties_service),
) -> Page[ShiftPenaltyReadSchema]:
    """Получить список штрафов с фильтрацией и пагинацией."""
    filters = ShiftPenaltyFilterSchema(
        scheduled_shift_id=scheduled_shift_id,
        type=penalty_type,
        penalty_points_min=penalty_points_min,
        penalty_points_max=penalty_points_max,
        detected_at_from=detected_at_from,
        detected_at_to=detected_at_to,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
    )
    return await service.get_penalties(params=params, filters=filters)


@shift_penalties_router.get(
    "/shift/{scheduled_shift_id}",
    response_model=list[ShiftPenaltyReadSchema],
)
async def get_penalties_by_shift(
    scheduled_shift_id: int,
    service: ShiftPenaltiesService = Depends(get_shift_penalties_service),
) -> list[ShiftPenaltyReadSchema]:
    """Получить все штрафы для конкретной запланированной смены."""
    return await service.get_penalties_by_shift_id(scheduled_shift_id)


@shift_penalties_router.get(
    "/shift/{scheduled_shift_id}/summary",
    response_model=ShiftPenaltySummarySchema,
)
async def get_penalties_summary(
    scheduled_shift_id: int,
    service: ShiftPenaltiesService = Depends(get_shift_penalties_service),
) -> ShiftPenaltySummarySchema:
    """Получить сводку штрафов для конкретной запланированной смены."""
    return await service.get_summary_by_shift_id(scheduled_shift_id)


@shift_penalties_router.get(
    "/{penalty_id}",
    response_model=ShiftPenaltyReadSchema,
)
async def get_penalty(
    penalty_id: int,
    service: ShiftPenaltiesService = Depends(get_shift_penalties_service),
) -> ShiftPenaltyReadSchema:
    """Получить штраф по ID."""
    return await service.get_penalty_by_id(penalty_id)


@shift_penalties_router.patch(
    "/{penalty_id}",
    response_model=ShiftPenaltyReadSchema,
)
async def update_penalty(
    penalty_id: int,
    data: ShiftPenaltyUpdateSchema,
    service: ShiftPenaltiesService = Depends(get_shift_penalties_service),
) -> ShiftPenaltyReadSchema:
    """Обновить существующий штраф."""
    return await service.update_penalty(penalty_id, data)


@shift_penalties_router.delete(
    "/{penalty_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_penalty(
    penalty_id: int,
    service: ShiftPenaltiesService = Depends(get_shift_penalties_service),
) -> None:
    """Удалить штраф."""
    await service.delete_penalty(penalty_id)
