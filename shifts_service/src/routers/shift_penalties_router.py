from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.schemas.shift_penalties_schemas import (
    PenaltyCreateSchema,
    PenaltyFilterSchema,
    PenaltyReadSchema,
    PenaltySummarySchema,
    PenaltyUpdateSchema,
)
from src.services.shift_penalties_service import PenaltiesService
from src.utils.dependencies import get_penalties_service

penalties_router = APIRouter(prefix="/penalties", tags=["Penalties"])


@penalties_router.post(
    "",
    response_model=PenaltyReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_penalty(
    data: PenaltyCreateSchema,
    service: PenaltiesService = Depends(get_penalties_service),
) -> PenaltyReadSchema:
    """Создать новый штраф для сотрудника."""
    return await service.create_penalty(data)


@penalties_router.get(
    "",
    response_model=Page[PenaltyReadSchema],
)
async def get_penalties(
    params: Params = Depends(),
    employee_id: int | None = Query(None, description="ID сотрудника"),
    created_at_from: datetime | None = Query(None, description="Дата создания от"),
    created_at_to: datetime | None = Query(None, description="Дата создания до"),
    service: PenaltiesService = Depends(get_penalties_service),
) -> Page[PenaltyReadSchema]:
    """Получить список штрафов с фильтрацией и пагинацией."""
    filters = PenaltyFilterSchema(
        employee_id=employee_id,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
    )
    return await service.get_penalties(params=params, filters=filters)


@penalties_router.get(
    "/employee/{employee_id}",
    response_model=list[PenaltyReadSchema],
)
async def get_penalties_by_employee(
    employee_id: int,
    service: PenaltiesService = Depends(get_penalties_service),
) -> list[PenaltyReadSchema]:
    """Получить все штрафы для конкретного сотрудника."""
    return await service.get_penalties_by_employee_id(employee_id)


@penalties_router.get(
    "/employee/{employee_id}/summary",
    response_model=PenaltySummarySchema,
)
async def get_penalties_summary(
    employee_id: int,
    service: PenaltiesService = Depends(get_penalties_service),
) -> PenaltySummarySchema:
    """Получить сводку штрафов для конкретного сотрудника."""
    return await service.get_summary_by_employee_id(employee_id)


@penalties_router.get(
    "/{penalty_id}",
    response_model=PenaltyReadSchema,
)
async def get_penalty(
    penalty_id: int,
    service: PenaltiesService = Depends(get_penalties_service),
) -> PenaltyReadSchema:
    """Получить штраф по ID."""
    return await service.get_penalty_by_id(penalty_id)


@penalties_router.patch(
    "/{penalty_id}",
    response_model=PenaltyReadSchema,
)
async def update_penalty(
    penalty_id: int,
    data: PenaltyUpdateSchema,
    service: PenaltiesService = Depends(get_penalties_service),
) -> PenaltyReadSchema:
    """Обновить существующий штраф."""
    return await service.update_penalty(penalty_id, data)


@penalties_router.delete(
    "/{penalty_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_penalty(
    penalty_id: int,
    service: PenaltiesService = Depends(get_penalties_service),
) -> None:
    """Удалить штраф."""
    await service.delete_penalty(penalty_id)
