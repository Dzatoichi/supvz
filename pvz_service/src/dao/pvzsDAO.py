from typing import Optional

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.employees.employees import Employees, employee_pvz_association
from src.models.pvzs.PVZs import PVZs


class PVZsDAO(BaseDAO[PVZs]):
    """
    Класс, наследующий базовый DAO для работы с сущностями ПВЗ.
    """

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
    async def get_pvzs(self, params: Params, *args, **kwargs) -> Optional[list[PVZs]]:
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

            stmt = stmt.order_by(self.model.id)

            return await apaginate(session, stmt, params)

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
            return await apaginate(session, stmt, params)

    @BaseDAO.with_exception
    async def update_pvzs_responsible_by_group(self, group_id: int, responsible_id: int):
        """
        Обновляет поле responsible_id у всех ПВЗ, принадлежащих указанной группе.
        """
        async with self._get_session() as session:
            stmt = update(self.model).where(self.model.group_id == group_id).values(responsible_id=responsible_id)
            await session.execute(stmt)
            await session.commit()

    @BaseDAO.with_exception
    async def assign_pvz_to_group(self, group_id: int, pvz_ids: list[int]):
        """Привязывает пвз к указанной группе по ее ID"""

        async with self._get_session() as session:
            stmt = update(self.model).where(self.model.id.in_(pvz_ids)).values(group_id=group_id)
            await session.execute(stmt)
            await session.commit()

    @BaseDAO.with_exception
    async def set_responsible_for_group(
        self,
        group_id: int,
        responsible_id: int,
        session: AsyncSession,
    ):
        stmt = update(self.model).where(self.model.group_id == group_id).values(responsible_id=responsible_id)
        await session.execute(stmt)
