from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.shift_penalties import ShiftPenalty
from src.schemas.shift_penalties_schemas import (
    PenaltyCreateSchema,
    PenaltyFilterSchema,
    PenaltyReadSchema,
    PenaltySummarySchema,
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

        page = await paginate(self.session, stmt, params)
        return Page(
            items=[PenaltyReadSchema.model_validate(item) for item in page.items],
            total=page.total,
            page=page.page,
            pages=page.pages,
            size=page.size,
        )

    @BaseDAO.with_exception
    async def get_penalties_by_employee_id(
        self,
        employee_id: int,
    ) -> list[PenaltyReadSchema]:
        """Получение всех штрафов по ID сотрудника."""
        stmt = (
            select(self.model)
            .where(self.model.employee_id == employee_id)
            .order_by(self.model.created_at.desc())
        )

        result = await self.session.execute(stmt)
        penalties = result.scalars().all()
        return [PenaltyReadSchema.model_validate(p) for p in penalties]

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

    @BaseDAO.with_exception
    async def get_summary_by_employee_id(
        self,
        employee_id: int,
    ) -> PenaltySummarySchema:
        """Получение сводки штрафов по ID сотрудника."""
        stmt = select(
            func.count(self.model.id).label("total_penalties"),
        ).where(self.model.employee_id == employee_id)

        result = await self.session.execute(stmt)
        row = result.one()

        return PenaltySummarySchema(
            total_penalties=row.total_penalties,
        )
