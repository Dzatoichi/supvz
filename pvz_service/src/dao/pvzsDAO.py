from typing import Optional

from sqlalchemy import select, update

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
    async def unassign_pvzs_from_group(self, group_id: int):
        """
        Отвязывает все ПВЗ от указанной группы, устанавливая group_id в None.
        """
        async with self._get_session() as session:
            stmt = update(self.model).where(self.model.group_id == group_id).values(group_id=None)
            await session.execute(stmt)
            await session.commit()

    @BaseDAO.with_exception
    async def get_employees_by_pvz_id(self, pvz_id: int):
        async with self._get_session() as session:
            stmt = (
                select(Employees)
                .join(
                    employee_pvz_association,
                    Employees.user_id == employee_pvz_association.c.employee_id,
                )
                .where(employee_pvz_association.c.pvz_id == pvz_id)
            )
            result = await session.scalars(stmt)
            return result.all()
