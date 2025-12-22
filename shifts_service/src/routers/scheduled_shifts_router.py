from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.dao.ScheduledShiftsDAO import ScheduledShiftsDAO
from src.schemas.scheduled_shifts_schemas import (
    ScheduledShiftCreateSchema,
    ScheduledShiftReadSchema,
    ScheduledShiftUpdateSchema,
)
from src.services.scheduled_shifts_service import ScheduledShiftsService
from src.utils.dependencies import get_scheduled_shifts_dao, get_scheduled_shifts_service

scheduled_shifts_router = APIRouter(
    prefix="/scheduled_shifts",
    tags=["Scheduled Shifts"],
)


@scheduled_shifts_router.post(
    "/",
    response_model=ScheduledShiftReadSchema,
)
async def create_scheduled_shift(
    scheduled_shift: ScheduledShiftCreateSchema,
    scheduled_shifts_service: ScheduledShiftsService = Depends(get_scheduled_shifts_service),
    repo: ScheduledShiftsDAO = Depends(get_scheduled_shifts_dao),
) -> ScheduledShiftReadSchema:
    """
    Ручка создания запланированной смены
    POST [/scheduled_shifts]
    """

    result = await scheduled_shifts_service.create_scheduled_shift(
        scheduled_shift=scheduled_shift,
        repo=repo,
    )
    return result


@scheduled_shifts_router.get(
    "/",
    response_model=Page[ScheduledShiftReadSchema],
)
async def get_scheduled_shifts(
    user_id: int = Query(None, description="ID пользователя создавшего смену"),
    pvz_id: int = Query(None, description="ID ПВЗ"),
    starts_at: datetime = Query(None, description="Начало смены"),
    ends_at: datetime = Query(None, description="<Конец смены"),
    completed: bool = Query(None, description="Статус завершенности смены"),
    status: str = Query(None, pattern="^(scheduled|completed|missed|cancelled)$", description="Статус смены"),
    paid: bool = Query(None, description="Статус оплаты смены"),
    scheduled_shifts_service: ScheduledShiftsService = Depends(get_scheduled_shifts_service),
    repo: ScheduledShiftsDAO = Depends(get_scheduled_shifts_dao),
    params: Params = Depends(),
) -> Page[ScheduledShiftReadSchema]:
    """
    Ручка получения всех запланированных смен с фильтрацией и пагинацией
    GET [/scheduled_shifts]
    """

    result = await scheduled_shifts_service.get_scheduled_shifts(
        user_id=user_id,
        pvz_id=pvz_id,
        starts_at=starts_at,
        ends_at=ends_at,
        completed=completed,
        status=status,
        paid=paid,
        repo=repo,
        params=params,
    )
    return result


@scheduled_shifts_router.get(
    "/{scheduled_shift_id}",
    response_model=ScheduledShiftReadSchema,
)
async def get_scheduled_shift(
    scheduled_shift_id: int,
    scheduled_shift_service: ScheduledShiftsService = Depends(get_scheduled_shifts_service),
    repo: ScheduledShiftsDAO = Depends(get_scheduled_shifts_dao),
) -> ScheduledShiftReadSchema:
    """
    Ручка получения запланированной смены
    GET [/scheduled_shifts/{scheduled_shift_id}]
    """

    scheduled_shift = await scheduled_shift_service.get_scheduled_shift_by_id(
        scheduled_shift_id=scheduled_shift_id,
        repo=repo,
    )
    return scheduled_shift


@scheduled_shifts_router.patch(
    "/{scheduled_shift_id}",
    response_model=ScheduledShiftReadSchema,
)
async def update_scheduled_shift(
    scheduled_shift_id: int,
    scheduled_shift: ScheduledShiftUpdateSchema,
    scheduled_shifts_service: ScheduledShiftsService = Depends(get_scheduled_shifts_service),
    repo: ScheduledShiftsDAO = Depends(get_scheduled_shifts_dao),
) -> ScheduledShiftReadSchema:
    """
    Ручка обновления запланированной смены
    PATCH [/scheduled_shifts]
    """

    result = await scheduled_shifts_service.update_scheduled_shift(
        scheduled_shift_id=scheduled_shift_id,
        updated_data=scheduled_shift,
        repo=repo,
    )
    return result


@scheduled_shifts_router.delete(
    "/{scheduled_shift_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_scheduled_shift(
    scheduled_shift_id: int,
    scheduled_shifts_service: ScheduledShiftsService = Depends(get_scheduled_shifts_service),
    repo: ScheduledShiftsDAO = Depends(get_scheduled_shifts_dao),
) -> None:
    """
    Ручка удаления запланированной смены\
    DELETE [/scheduled_shifts/{scheduled_shift_id}]
    """

    result = await scheduled_shifts_service.delete_scheduled_shift(
        scheduled_shift_id=scheduled_shift_id,
        repo=repo,
    )
    return result
