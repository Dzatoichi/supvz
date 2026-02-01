from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.schemas.shift_requests_schemas import (
    RequestStatusEnum,
    RequestTypeEnum,
    ShiftRequestCancelByUserSchema,
    ShiftRequestCreateSchema,
    ShiftRequestFilterSchema,
    ShiftRequestProcessSchema,
    ShiftRequestReadSchema,
    ShiftRequestUpdateSchema,
)
from src.services.shift_requests_service import ShiftRequestsService
from src.utils.dependencies import get_shift_requests_service

shift_requests_router = APIRouter(prefix="/shift-requests", tags=["Shift Requests"])


@shift_requests_router.post(
    "",
    response_model=ShiftRequestReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_shift_request(
    data: ShiftRequestCreateSchema,
    service: ShiftRequestsService = Depends(get_shift_requests_service),
) -> ShiftRequestReadSchema:
    """
    Создать новый запрос на смену.

    - **add**: запрос на добавление смены (scheduled_shift_id опционален)
    - **cancel**: запрос на отмену смены (scheduled_shift_id обязателен)
    - **change**: запрос на передачу смены другому (scheduled_shift_id и new_user_id обязательны)

    Нельзя создать запрос на cancel/change если смена уже началась.
    """
    return await service.create_request(data)


@shift_requests_router.get(
    "",
    response_model=Page[ShiftRequestReadSchema],
)
async def get_shift_requests(
    params: Params = Depends(),
    user_id: int | None = Query(None, description="ID пользователя"),
    scheduled_shift_id: int | None = Query(None, description="ID запланированной смены"),
    request_type: RequestTypeEnum | None = Query(None, description="Тип запроса"),
    request_status: RequestStatusEnum | None = Query(
        None,
        alias="status",
        description="Статус запроса",
    ),
    requested_at_from: datetime | None = Query(None, description="Дата запроса от"),
    requested_at_to: datetime | None = Query(None, description="Дата запроса до"),
    scheduled_shift_start_time_from: datetime | None = Query(
        None,
        description="Время начала смены от",
    ),
    scheduled_shift_start_time_to: datetime | None = Query(
        None,
        description="Время начала смены до",
    ),
    service: ShiftRequestsService = Depends(get_shift_requests_service),
) -> Page[ShiftRequestReadSchema]:
    """Получить список запросов на смену с фильтрацией и пагинацией."""
    filters = ShiftRequestFilterSchema(
        user_id=user_id,
        scheduled_shift_id=scheduled_shift_id,
        request_type=request_type,
        status=request_status,
        requested_at_from=requested_at_from,
        requested_at_to=requested_at_to,
        scheduled_shift_start_time_from=scheduled_shift_start_time_from,
        scheduled_shift_start_time_to=scheduled_shift_start_time_to,
    )
    return await service.get_requests(params=params, filters=filters)


@shift_requests_router.get(
    "/{request_id}",
    response_model=ShiftRequestReadSchema,
)
async def get_shift_request(
    request_id: int,
    service: ShiftRequestsService = Depends(get_shift_requests_service),
) -> ShiftRequestReadSchema:
    """Получить запрос на смену по ID."""
    return await service.get_request_by_id(request_id)


@shift_requests_router.patch(
    "/{request_id}",
    response_model=ShiftRequestReadSchema,
)
async def update_shift_request(
    request_id: int,
    data: ShiftRequestUpdateSchema,
    service: ShiftRequestsService = Depends(get_shift_requests_service),
) -> ShiftRequestReadSchema:
    """
    Обновить существующий запрос на смену.

    Можно обновлять только pending запросы.
    """
    return await service.update_request(request_id, data)


@shift_requests_router.post(
    "/{request_id}/process",
    response_model=ShiftRequestReadSchema,
)
async def process_shift_request(
    request_id: int,
    data: ShiftRequestProcessSchema,
    service: ShiftRequestsService = Depends(get_shift_requests_service),
) -> ShiftRequestReadSchema:
    """
    Обработать запрос на смену (одобрить или отклонить).

    - Можно обрабатывать только pending запросы.
    - Нельзя одобрить cancel/change если смена уже началась.
    """
    return await service.process_request(request_id, data)


@shift_requests_router.post(
    "/{request_id}/cancel",
    response_model=ShiftRequestReadSchema,
)
async def cancel_shift_request_by_user(
    request_id: int,
    user_id: int = Query(..., description="ID пользователя, отменяющего запрос"),
    data: ShiftRequestCancelByUserSchema | None = None,
    service: ShiftRequestsService = Depends(get_shift_requests_service),
) -> ShiftRequestReadSchema:
    """
    Отменить запрос на смену пользователем.

    Пользователь может отменить только свой pending запрос.
    """
    return await service.cancel_request_by_user(request_id, user_id, data)


@shift_requests_router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_shift_request(
    request_id: int,
    service: ShiftRequestsService = Depends(get_shift_requests_service),
) -> None:
    """Удалить запрос на смену."""
    await service.delete_request(request_id)
