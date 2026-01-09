from fastapi_pagination import Page, Params

from src.dao.shiftsDAO import ShiftsDAO
from src.schemas.shifts_schemas import (
    ShiftCreateSchema,
    ShiftFilterSchema,
    ShiftReadSchema,
    ShiftUpdateSchema,
)
from src.utils.exceptions import ShiftNotFoundException


class ShiftsService:
    """Сервис для бизнес-логики работы со сменами."""

    def __init__(self, dao: ShiftsDAO):
        """Инициализация сервиса."""
        self.dao = dao

    async def create_shift(self, data: ShiftCreateSchema) -> ShiftReadSchema:
        """Создание смены."""
        return await self.dao.create_shift(data)

    async def get_shift_by_id(self, shift_id: int) -> ShiftReadSchema:
        """Получение смены по ID."""
        shift = await self.dao.get_shift_by_id(shift_id)
        if not shift:
            raise ShiftNotFoundException()
        return shift

    async def get_shifts(
        self,
        params: Params,
        filters: ShiftFilterSchema | None = None,
    ) -> Page[ShiftReadSchema]:
        """Получение списка смен."""
        return await self.dao.get_shifts_paginated(params=params, filters=filters)

    async def update_shift(
        self,
        shift_id: int,
        data: ShiftUpdateSchema,
    ) -> ShiftReadSchema:
        """Обновление смены."""
        existing = await self.dao.get_shift_by_id(shift_id)
        if not existing:
            raise ShiftNotFoundException()
        updated = await self.dao.update_shift(shift_id, data)
        if not updated:
            raise ShiftNotFoundException()
        return updated

    async def delete_shift(self, shift_id: int) -> bool:
        """Удаление смены."""
        existing = await self.dao.get_shift_by_id(shift_id)
        if not existing:
            raise ShiftNotFoundException()
        return await self.dao.delete_shift(shift_id)
