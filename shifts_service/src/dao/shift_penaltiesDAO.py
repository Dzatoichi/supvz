from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.shift_penalties import ShiftPenalty
from src.schemas.shift_penalties_schemas import (
    PenaltyTypeEnum,
    ShiftPenaltyCreateSchema,
    ShiftPenaltyFilterSchema,
    ShiftPenaltyReadSchema,
    ShiftPenaltySummarySchema,
    ShiftPenaltyUpdateSchema,
)


class ShiftPenaltiesDAO(BaseDAO[ShiftPenalty]):
    """DAO для работы со штрафами смен."""

    def __init__(self, session: AsyncSession):
        """Инициализация ShiftPenaltiesDAO."""
        super().__init__(session=session, model=ShiftPenalty)

    @BaseDAO.with_exception
    async def create_penalty(self, data: ShiftPenaltyCreateSchema) -> ShiftPenaltyReadSchema:
        """Создание нового штрафа."""
        obj = await super().create(data)
        return ShiftPenaltyReadSchema.model_validate(obj)

    @BaseDAO.with_exception
    async def get_penalty_by_id(self, penalty_id: int) -> ShiftPenaltyReadSchema | None:
        """Получение штрафа по ID."""
        obj = await super().get_by_id(penalty_id)
        if obj:
            return ShiftPenaltyReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def get_penalties_paginated(
        self,
        params: Params,
        filters: ShiftPenaltyFilterSchema | None = None,
    ) -> Page[ShiftPenaltyReadSchema]:
        """Получение списка штрафов с пагинацией и фильтрацией."""
        stmt = select(self.model)

        if filters:
            if filters.scheduled_shift_id is not None:
                stmt = stmt.where(self.model.scheduled_shift_id == filters.scheduled_shift_id)
            if filters.type is not None:
                stmt = stmt.where(self.model.type == filters.type.value)
            if filters.penalty_points_min is not None:
                stmt = stmt.where(self.model.penalty_points >= filters.penalty_points_min)
            if filters.penalty_points_max is not None:
                stmt = stmt.where(self.model.penalty_points <= filters.penalty_points_max)
            if filters.detected_at_from is not None:
                stmt = stmt.where(self.model.detected_at >= filters.detected_at_from)
            if filters.detected_at_to is not None:
                stmt = stmt.where(self.model.detected_at <= filters.detected_at_to)
            if filters.created_at_from is not None:
                stmt = stmt.where(self.model.created_at >= filters.created_at_from)
            if filters.created_at_to is not None:
                stmt = stmt.where(self.model.created_at <= filters.created_at_to)

        stmt = stmt.order_by(self.model.id.desc())

        page = await paginate(self.session, stmt, params)
        return Page(
            items=[ShiftPenaltyReadSchema.model_validate(item) for item in page.items],
            total=page.total,
            page=page.page,
            pages=page.pages,
            size=page.size,
        )

    @BaseDAO.with_exception
    async def get_penalties_by_shift_id(
        self,
        scheduled_shift_id: int,
    ) -> list[ShiftPenaltyReadSchema]:
        """Получение всех штрафов по ID запланированной смены."""
        stmt = (
            select(self.model)
            .where(self.model.scheduled_shift_id == scheduled_shift_id)
            .order_by(self.model.detected_at.desc())
        )

        result = await self.session.execute(stmt)
        penalties = result.scalars().all()
        return [ShiftPenaltyReadSchema.model_validate(p) for p in penalties]

    @BaseDAO.with_exception
    async def update_penalty(
        self,
        penalty_id: int,
        data: ShiftPenaltyUpdateSchema,
    ) -> ShiftPenaltyReadSchema | None:
        """Обновление данных штрафа."""
        obj = await super().update(penalty_id, data)
        if obj:
            return ShiftPenaltyReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def delete_penalty(self, penalty_id: int) -> bool:
        """Удаление штрафа."""
        return await super().delete(penalty_id)

    @BaseDAO.with_exception
    async def get_summary_by_shift_id(
        self,
        scheduled_shift_id: int,
    ) -> ShiftPenaltySummarySchema:
        """Получение сводки штрафов по ID запланированной смены."""
        stmt = select(
            func.count(self.model.id).label("total_penalties"),
            func.coalesce(func.sum(self.model.penalty_points), 0).label("total_points"),
            func.count(self.model.id)
            .filter(self.model.type == PenaltyTypeEnum.LATE_START.value)
            .label("late_start_count"),
            func.count(self.model.id)
            .filter(self.model.type == PenaltyTypeEnum.EARLY_END.value)
            .label("early_end_count"),
            func.count(self.model.id).filter(self.model.type == PenaltyTypeEnum.MISS.value).label("miss_count"),
            func.count(self.model.id).filter(self.model.type == PenaltyTypeEnum.OTHER.value).label("other_count"),
            func.coalesce(
                func.sum(self.model.penalty_minutes).filter(self.model.type == PenaltyTypeEnum.LATE_START.value), 0
            ).label("total_late_minutes"),
        ).where(self.model.scheduled_shift_id == scheduled_shift_id)

        result = await self.session.execute(stmt)
        row = result.one()

        return ShiftPenaltySummarySchema(
            total_penalties=row.total_penalties,
            total_points=row.total_points,
            late_start_count=row.late_start_count,
            early_end_count=row.early_end_count,
            miss_count=row.miss_count,
            other_count=row.other_count,
            total_late_minutes=row.total_late_minutes,
        )
