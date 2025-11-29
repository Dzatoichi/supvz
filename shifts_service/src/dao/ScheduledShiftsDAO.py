from datetime import datetime

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, select

from src.dao.baseDAO import BaseDAO
from src.models.scheduled_shifts import ScheduledShifts


class ScheduledShiftsDAO(BaseDAO[ScheduledShifts]):
    def __init__(self):
        super().__init__(model=ScheduledShifts)

    @BaseDAO.with_exception
    async def get_scheduled_shifts_filtered(
        self,
        user_id: int | None,
        pvz_id: int | None,
        starts_at: datetime | None,
        ends_at: datetime | None,
        completed: bool | None,
        status: str | None,
        paid: bool | None,
        params: Params,
    ):
        async with self._get_session() as session:
            stmt = select(self.model)

            filter_conditions = []

            if user_id is not None:
                filter_conditions.append(self.model.user_id == user_id)
            if pvz_id is not None:
                filter_conditions.append(self.model.pvz_id == pvz_id)
            if starts_at is not None:
                filter_conditions.append(self.model.starts_at >= starts_at)
            if ends_at is not None:
                filter_conditions.append(self.model.ends_at <= ends_at)
            if completed is not None:
                filter_conditions.append(self.model.completed == completed)
            if status is not None:
                filter_conditions.append(self.model.status == status)
            if paid is not None:
                filter_conditions.append(self.model.paid == paid)

            if filter_conditions:
                stmt = stmt.where(and_(*filter_conditions))

            stmt = stmt.order_by(self.model.starts_at.desc(), self.model.created_at.desc())

            return await paginate(session, stmt, params=params)
