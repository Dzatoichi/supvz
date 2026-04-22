from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.shifts import Shift
from src.schemas.shifts_schemas import (
    ShiftCreateSchema,
    ShiftFilterSchema,
    ShiftReadSchema,
    ShiftUpdateSchema,
)


class ShiftsDAO(BaseDAO[Shift]):
    """DAO для работы со сменами."""

    def __init__(self, session: AsyncSession):
        """Инициализация ShiftsDAO."""
        super().__init__(session=session, model=Shift)

    @BaseDAO.with_exception
    async def create_shift(self, data: ShiftCreateSchema) -> ShiftReadSchema:
        """Создание новой смены."""
        obj = await super().create(data)
        return ShiftReadSchema.model_validate(obj)

    @BaseDAO.with_exception
    async def get_shift_by_id(self, shift_id: int) -> ShiftReadSchema | None:
        """Получение смены по ID."""
        obj = await super().get_by_id(shift_id)
        if obj:
            return ShiftReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def get_shifts_paginated(
        self,
        params: Params,
        filters: ShiftFilterSchema | None = None,
    ) -> Page[ShiftReadSchema]:
        """Получение списка смен с пагинацией и фильтрацией."""
        stmt = select(self.model)

        if filters:
            if filters.scheduled_shift_id is not None:
                stmt = stmt.where(self.model.scheduled_shift_id == filters.scheduled_shift_id)
            if filters.started_at_from is not None:
                stmt = stmt.where(self.model.started_at >= filters.started_at_from)
            if filters.started_at_to is not None:
                stmt = stmt.where(self.model.started_at <= filters.started_at_to)
            if filters.ended_at_from is not None:
                stmt = stmt.where(self.model.ended_at >= filters.ended_at_from)
            if filters.ended_at_to is not None:
                stmt = stmt.where(self.model.ended_at <= filters.ended_at_to)
            if filters.is_active is not None:
                if filters.is_active:
                    stmt = stmt.where(self.model.ended_at.is_(None))
                else:
                    stmt = stmt.where(self.model.ended_at.isnot(None))

        stmt = stmt.order_by(self.model.id.desc())

        page = await paginate(self.session, stmt, params)
        return Page(
            items=[ShiftReadSchema.model_validate(item) for item in page.items],
            total=page.total,
            page=page.page,
            pages=page.pages,
            size=page.size,
        )

    @BaseDAO.with_exception
    async def update_shift(self, shift_id: int, data: ShiftUpdateSchema) -> ShiftReadSchema | None:
        """Обновление данных смены."""
        obj = await super().update(shift_id, data)
        if obj:
            return ShiftReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def delete_shift(self, shift_id: int) -> bool:
        """Удаление смены."""
        return await super().delete(shift_id)
