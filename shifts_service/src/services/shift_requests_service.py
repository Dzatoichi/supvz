from datetime import datetime

from fastapi_pagination import Page, Params

from src.dao.shift_requestsDAO import ShiftRequestsDAO
from src.schemas.shift_requests_schemas import (
    RequestStatusEnum,
    RequestTypeEnum,
    ShiftRequestCreateSchema,
    ShiftRequestFilterSchema,
    ShiftRequestProcessSchema,
    ShiftRequestReadSchema,
    ShiftRequestUpdateSchema,
)
from src.utils.exceptions import (
    ShiftRequestAlreadyExistsException,
    ShiftRequestAlreadyProcessedException,
    ShiftRequestNotFoundException,
    ShiftRequestShiftAlreadyStartedException,
    ShiftRequestValidationException,
)


class ShiftRequestsService:
    """Сервис для бизнес-логики работы с запросами на смены."""

    def __init__(self, dao: ShiftRequestsDAO):
        """Инициализация сервиса."""
        self.dao = dao

    async def create_request(
        self,
        data: ShiftRequestCreateSchema,
    ) -> ShiftRequestReadSchema:
        """
        Создание запроса на смену.
        """
        current_time = datetime.now()

        if data.request_type in (RequestTypeEnum.CANCEL, RequestTypeEnum.CHANGE):
            if data.scheduled_shift_start_time <= current_time:
                raise ShiftRequestShiftAlreadyStartedException(
                    "Нельзя создать запрос на отмену/изменение: смена уже началась",
                )

        is_duplicate = await self.dao.check_duplicate_pending_request(
            user_id=data.user_id,
            scheduled_shift_id=data.scheduled_shift_id,
            request_type=data.request_type.value,
            scheduled_shift_start_time=data.scheduled_shift_start_time,
        )
        if is_duplicate:
            raise ShiftRequestAlreadyExistsException("Аналогичный запрос уже существует и ожидает обработки")

        return await self.dao.create_request(data)

    async def get_request_by_id(self, request_id: int) -> ShiftRequestReadSchema:
        """Получение запроса по ID."""
        request = await self.dao.get_request_by_id(request_id)
        if not request:
            raise ShiftRequestNotFoundException()
        return request

    async def get_requests(
        self,
        params: Params,
        filters: ShiftRequestFilterSchema | None = None,
    ) -> Page[ShiftRequestReadSchema]:
        """Получение списка запросов."""
        return await self.dao.get_requests_paginated(params=params, filters=filters)

    async def update_request(
        self,
        request_id: int,
        data: ShiftRequestUpdateSchema,
    ) -> ShiftRequestReadSchema:
        """
        Обновление запроса.

        Можно обновлять только pending запросы.
        """
        existing = await self.dao.get_request_by_id(request_id)
        if not existing:
            raise ShiftRequestNotFoundException()

        if existing.status != RequestStatusEnum.PENDING:
            raise ShiftRequestAlreadyProcessedException("Нельзя обновить уже обработанный запрос")

        updated = await self.dao.update_request(request_id, data)
        if not updated:
            raise ShiftRequestNotFoundException()
        return updated

    async def process_request(
        self,
        request_id: int,
        data: ShiftRequestProcessSchema,
    ) -> ShiftRequestReadSchema:
        """
        Обработка запроса (одобрение/отклонение).
        """
        existing = await self.dao.get_request_by_id(request_id)
        if not existing:
            raise ShiftRequestNotFoundException()

        if existing.status != RequestStatusEnum.PENDING:
            raise ShiftRequestAlreadyProcessedException("Запрос уже обработан")

        current_time = datetime.now()

        if data.status == RequestStatusEnum.APPROVED:
            if existing.request_type in (
                RequestTypeEnum.CANCEL,
                RequestTypeEnum.CHANGE,
            ):
                if existing.scheduled_shift_start_time <= current_time:
                    raise ShiftRequestShiftAlreadyStartedException("Нельзя одобрить запрос: смена уже началась")

        updated = await self.dao.update_request_status(
            request_id=request_id,
            status=data.status.value,
            processed_by=data.processed_by,
            response=data.response,
        )
        if not updated:
            raise ShiftRequestNotFoundException()
        return updated

    async def cancel_request_by_user(
        self,
        request_id: int,
        user_id: int,
    ) -> ShiftRequestReadSchema:
        """
        Отмена запроса пользователем.
        """
        existing = await self.dao.get_request_by_id(request_id)
        if not existing:
            raise ShiftRequestNotFoundException()

        if existing.user_id != user_id:
            raise ShiftRequestValidationException("Нельзя отменить чужой запрос")

        if existing.status != RequestStatusEnum.PENDING:
            raise ShiftRequestAlreadyProcessedException("Нельзя отменить уже обработанный запрос")

        updated = await self.dao.update_request_status(
            request_id=request_id,
            status=RequestStatusEnum.CANCELLED_BY_USER.value,
        )
        if not updated:
            raise ShiftRequestNotFoundException()
        return updated

    async def delete_request(self, request_id: int) -> None:
        """Удаление запроса."""
        existing = await self.dao.get_request_by_id(request_id)
        if not existing:
            raise ShiftRequestNotFoundException()
        await self.dao.delete_request(request_id)
