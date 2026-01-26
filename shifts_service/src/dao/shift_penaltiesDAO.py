from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.shift_penalties import ShiftPenalty
from src.schemas.shift_penalties_schemas import (
    PenaltyCreateSchema,
    PenaltyFilterSchema,
    PenaltyReadSchema,
    PenaltyUpdateSchema,
)


class PenaltiesDAO(BaseDAO[ShiftPenalty]):
    """DAO для работы со штрафами сотрудников."""

    def __init__(self, session: AsyncSession):
        """Инициализация PenaltiesDAO."""
        super().__init__(session=session, model=ShiftPenalty)

    @BaseDAO.with_exception
    async def create_penalty(self, data: PenaltyCreateSchema) -> PenaltyReadSchema:
        """Создание нового штрафа."""
        obj = await super().create(data)
        return PenaltyReadSchema.model_validate(obj)

    @BaseDAO.with_exception
    async def get_penalty_by_id(self, penalty_id: int) -> PenaltyReadSchema | None:
        """Получение штрафа по ID."""
        obj = await super().get_by_id(penalty_id)
        if obj:
            return PenaltyReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def get_penalties_paginated(
        self,
        params: Params,
        filters: PenaltyFilterSchema | None = None,
    ) -> Page[PenaltyReadSchema]:
        """Получение списка штрафов с пагинацией и фильтрацией."""
        stmt = select(self.model)

        if filters:
            if filters.employee_id is not None:
                stmt = stmt.where(self.model.employee_id == filters.employee_id)
            if filters.created_at_from is not None:
                stmt = stmt.where(self.model.created_at >= filters.created_at_from)
            if filters.created_at_to is not None:
                stmt = stmt.where(self.model.created_at <= filters.created_at_to)

        stmt = stmt.order_by(self.model.id.desc())

        return await paginate(self.session, stmt, params)

    @BaseDAO.with_exception
    async def update_penalty(
        self,
        penalty_id: int,
        data: PenaltyUpdateSchema,
    ) -> PenaltyReadSchema | None:
        """Обновление данных штрафа."""
        obj = await super().update(penalty_id, data)
        if obj:
            return PenaltyReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def delete_penalty(self, penalty_id: int) -> bool:
        """Удаление штрафа."""
        return await super().delete(penalty_id)
