from typing import Optional

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from src.dao.baseDAO import BaseDAO
from src.models.employees.employees import Employees, employee_pvz_association
from src.models.pvzs.PVZs import PVZs


class PVZsDAO(BaseDAO[PVZs]):
    def __init__(self):
        super().__init__(model=PVZs)

    @BaseDAO.with_exception
    async def get_pvz(self, *args, **kwargs) -> Optional[PVZs]:
        """
        Данный метод реализует поиск по любому аттрибуту,
        который будет указан в качестве аргумента функции.
        """
        async with self._get_session() as session:
            stmt = select(self.model)
            if args:
                stmt = stmt.filter(*args)
            if kwargs:
                stmt = stmt.filter_by(**kwargs)

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @BaseDAO.with_exception
    async def get_pvzs(self, *args, **kwargs) -> Optional[list[PVZs]]:
        """
        Данный метод реализует поиск по любому аттрибуту,
        который будет указан в качестве аргумента функции.
        """
        async with self._get_session() as session:
            stmt = select(self.model)
            if args:
                stmt = stmt.filter(*args)
            if kwargs:
                stmt = stmt.filter_by(**kwargs)

            result = await session.execute(stmt)
            return result.scalars().all()

    @BaseDAO.with_exception
    async def get_employees_by_pvz_id(self, pvz_id: int, params: Params):
        async with self._get_session() as session:
            stmt = (
                select(Employees)
                .join(
                    employee_pvz_association,
                    Employees.user_id == employee_pvz_association.c.employee_id,
                )
                .where(employee_pvz_association.c.pvz_id == pvz_id)
            )
            return await paginate(session, stmt, params=params)
