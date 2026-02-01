from datetime import datetime

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.shift_requests import ShiftRequest
from src.schemas.shift_requests_schemas import (
    RequestStatusEnum,
    ShiftRequestCreateSchema,
    ShiftRequestFilterSchema,
    ShiftRequestReadSchema,
    ShiftRequestUpdateSchema,
)


class ShiftRequestsDAO(BaseDAO[ShiftRequest]):
    """DAO для работы с запросами на смены."""

    def __init__(self, session: AsyncSession):
        """Инициализация ShiftRequestsDAO."""
        super().__init__(session=session, model=ShiftRequest)

    @BaseDAO.with_exception
    async def create_request(
        self,
        data: ShiftRequestCreateSchema,
    ) -> ShiftRequestReadSchema:
        """Создание нового запроса на смену."""
        obj = await super().create(data)
        return ShiftRequestReadSchema.model_validate(obj)

    @BaseDAO.with_exception
    async def get_request_by_id(
        self,
        request_id: int,
    ) -> ShiftRequestReadSchema | None:
        """Получение запроса по ID."""
        obj = await super().get_by_id(request_id)
        if obj:
            return ShiftRequestReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def get_requests_paginated(
        self,
        params: Params,
        filters: ShiftRequestFilterSchema | None = None,
    ) -> Page[ShiftRequestReadSchema]:
        """Получение списка запросов с пагинацией и фильтрацией."""
        stmt = select(self.model)

        if filters:
            if filters.user_id is not None:
                stmt = stmt.where(self.model.user_id == filters.user_id)
            if filters.scheduled_shift_id is not None:
                stmt = stmt.where(self.model.scheduled_shift_id == filters.scheduled_shift_id)
            if filters.request_type is not None:
                stmt = stmt.where(self.model.request_type == filters.request_type.value)
            if filters.status is not None:
                stmt = stmt.where(self.model.status == filters.status.value)
            if filters.requested_at_from is not None:
                stmt = stmt.where(self.model.requested_at >= filters.requested_at_from)
            if filters.requested_at_to is not None:
                stmt = stmt.where(self.model.requested_at <= filters.requested_at_to)
            if filters.scheduled_shift_start_time_from is not None:
                stmt = stmt.where(self.model.scheduled_shift_start_time >= filters.scheduled_shift_start_time_from)
            if filters.scheduled_shift_start_time_to is not None:
                stmt = stmt.where(self.model.scheduled_shift_start_time <= filters.scheduled_shift_start_time_to)

        stmt = stmt.order_by(self.model.id.desc())

        page = await paginate(self.session, stmt, params)
        return Page(
            items=[ShiftRequestReadSchema.model_validate(item) for item in page.items],
            total=page.total,
            page=page.page,
            pages=page.pages,
            size=page.size,
        )

    @BaseDAO.with_exception
    async def update_request(
        self,
        request_id: int,
        data: ShiftRequestUpdateSchema,
    ) -> ShiftRequestReadSchema | None:
        """Обновление данных запроса."""
        obj = await super().update(request_id, data)
        if obj:
            return ShiftRequestReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def update_request_status(
        self,
        request_id: int,
        status: str,
        processed_by: int | None = None,
        reason: str | None = None,
    ) -> ShiftRequestReadSchema | None:
        """Обновление статуса запроса."""
        update_data = {
            "status": status,
            "processed_at": datetime.now(),
        }
        if processed_by is not None:
            update_data["processed_by"] = processed_by
        if reason is not None:
            update_data["reason"] = reason

        stmt = update(self.model).where(self.model.id == request_id).values(**update_data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        updated = result.scalar_one_or_none()
        if updated:
            await self.session.refresh(updated)
            return ShiftRequestReadSchema.model_validate(updated)
        return None

    @BaseDAO.with_exception
    async def delete_request(self, request_id: int) -> bool:
        """Удаление запроса."""
        return await super().delete(request_id)

    @BaseDAO.with_exception
    async def check_duplicate_pending_request(
        self,
        user_id: int,
        scheduled_shift_id: int | None,
        request_type: str,
        scheduled_shift_start_time: datetime,
    ) -> bool:
        """
        Проверяет наличие дублирующего pending запроса.
        """
        conditions = [
            self.model.user_id == user_id,
            self.model.request_type == request_type,
            self.model.status == RequestStatusEnum.PENDING.value,
        ]

        if scheduled_shift_id is not None:
            conditions.append(self.model.scheduled_shift_id == scheduled_shift_id)
        else:
            conditions.append(self.model.scheduled_shift_start_time == scheduled_shift_start_time)

        stmt = select(self.model).where(and_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
