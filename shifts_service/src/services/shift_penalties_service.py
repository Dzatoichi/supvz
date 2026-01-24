from fastapi_pagination import Page, Params

from src.dao.shift_penaltiesDAO import PenaltiesDAO
from src.schemas.shift_penalties_schemas import (
    PenaltyCreateSchema,
    PenaltyFilterSchema,
    PenaltyReadSchema,
    PenaltySummarySchema,
    PenaltyUpdateSchema,
)
from src.utils.exceptions import ShiftPenaltyNotFoundException


class PenaltiesService:
    """Сервис для бизнес-логики работы со штрафами сотрудников."""

    def __init__(self, dao: PenaltiesDAO):
        """Инициализация сервиса."""
        self.dao = dao

    async def create_penalty(
        self,
        data: PenaltyCreateSchema,
    ) -> PenaltyReadSchema:
        """Создание штрафа."""
        return await self.dao.create_penalty(data)

    async def get_penalty_by_id(self, penalty_id: int) -> PenaltyReadSchema:
        """Получение штрафа по ID."""
        penalty = await self.dao.get_penalty_by_id(penalty_id)
        if not penalty:
            raise ShiftPenaltyNotFoundException()
        return penalty

    async def get_penalties(
        self,
        params: Params,
        filters: PenaltyFilterSchema | None = None,
    ) -> Page[PenaltyReadSchema]:
        """Получение списка штрафов."""
        return await self.dao.get_penalties_paginated(params=params, filters=filters)

    async def get_penalties_by_employee_id(
        self,
        employee_id: int,
    ) -> list[PenaltyReadSchema]:
        """Получение штрафов по ID сотрудника."""
        return await self.dao.get_penalties_by_employee_id(employee_id)

    async def update_penalty(
        self,
        penalty_id: int,
        data: PenaltyUpdateSchema,
    ) -> PenaltyReadSchema:
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

    async def get_summary_by_employee_id(
        self,
        employee_id: int,
    ) -> PenaltySummarySchema:
        """Получение сводки штрафов по ID сотрудника."""
        return await self.dao.get_summary_by_employee_id(employee_id)
