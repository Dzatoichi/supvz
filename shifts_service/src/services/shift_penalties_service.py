from fastapi_pagination import Page, Params

from src.dao.shift_penaltiesDAO import ShiftPenaltiesDAO
from src.schemas.shift_penalties_schemas import (
    ShiftPenaltyCreateSchema,
    ShiftPenaltyFilterSchema,
    ShiftPenaltyReadSchema,
    ShiftPenaltySummarySchema,
    ShiftPenaltyUpdateSchema,
)
from src.utils.exceptions import ShiftPenaltyNotFoundException


class ShiftPenaltiesService:
    """Сервис для бизнес-логики работы со штрафами смен."""

    def __init__(self, dao: ShiftPenaltiesDAO):
        """Инициализация сервиса."""
        self.dao = dao

    async def create_penalty(
        self,
        data: ShiftPenaltyCreateSchema,
    ) -> ShiftPenaltyReadSchema:
        """Создание штрафа."""
        return await self.dao.create_penalty(data)

    async def get_penalty_by_id(self, penalty_id: int) -> ShiftPenaltyReadSchema:
        """Получение штрафа по ID."""
        penalty = await self.dao.get_penalty_by_id(penalty_id)
        if not penalty:
            raise ShiftPenaltyNotFoundException()
        return penalty

    async def get_penalties(
        self,
        params: Params,
        filters: ShiftPenaltyFilterSchema | None = None,
    ) -> Page[ShiftPenaltyReadSchema]:
        """Получение списка штрафов."""
        return await self.dao.get_penalties_paginated(params=params, filters=filters)

    async def get_penalties_by_shift_id(
        self,
        scheduled_shift_id: int,
    ) -> list[ShiftPenaltyReadSchema]:
        """Получение штрафов по ID запланированной смены."""
        return await self.dao.get_penalties_by_shift_id(scheduled_shift_id)

    async def update_penalty(
        self,
        penalty_id: int,
        data: ShiftPenaltyUpdateSchema,
    ) -> ShiftPenaltyReadSchema:
        """Обновление штрафа."""
        existing = await self.dao.get_penalty_by_id(penalty_id)
        if not existing:
            raise ShiftPenaltyNotFoundException()
        updated = await self.dao.update_penalty(penalty_id, data)
        if not updated:
            raise ShiftPenaltyNotFoundException()
        return updated

    async def delete_penalty(self, penalty_id: int) -> bool:
        """Удаление штрафа."""
        existing = await self.dao.get_penalty_by_id(penalty_id)
        if not existing:
            raise ShiftPenaltyNotFoundException()
        return await self.dao.delete_penalty(penalty_id)

    async def get_summary_by_shift_id(
        self,
        scheduled_shift_id: int,
    ) -> ShiftPenaltySummarySchema:
        """Получение сводки штрафов по ID запланированной смены."""
        return await self.dao.get_summary_by_shift_id(scheduled_shift_id)
