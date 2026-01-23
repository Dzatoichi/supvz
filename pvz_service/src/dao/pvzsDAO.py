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

    def __init__(self, session: AsyncSession):
        super().__init__(model=PVZs, session=session)

    @BaseDAO.with_exception
    async def get_pvz(self, *args, **kwargs) -> Optional[PVZs]:
        """
        Данный метод реализует поиск по любому аттрибуту,
        который будет указан в качестве аргумента функции.
        """
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @BaseDAO.with_exception
    async def get_pvzs(self, params: Params, *args, **kwargs) -> Optional[list[PVZs]]:
        """
        Данный метод реализует поиск по любому аттрибуту,
        который будет указан в качестве аргумента функции.
        """
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)

        stmt = stmt.order_by(self.model.id)

        return await apaginate(self.session, stmt, params)

    @BaseDAO.with_exception
    async def unassign_pvzs_from_group(self, group_id: int):
        """
        Отвязывает все ПВЗ от указанной группы, устанавливая group_id в None.
        """
        stmt = update(self.model).where(self.model.group_id == group_id).values(group_id=None)
        await self.session.execute(stmt)
        await self.session.commit()

    @BaseDAO.with_exception
    async def get_employees_by_pvz_id(self, pvz_id: int, params: Params):
        stmt = (
            select(Employees)
            .join(
                employee_pvz_association,
                Employees.user_id == employee_pvz_association.c.employee_id,
            )
            .where(employee_pvz_association.c.pvz_id == pvz_id)
        )
        return await apaginate(self.session, stmt, params)

    @BaseDAO.with_exception
    async def update_pvzs_responsible_by_group(self, group_id: int, responsible_id: int):
        """
        Обновляет поле responsible_id у всех ПВЗ, принадлежащих указанной группе.
        """
        stmt = update(self.model).where(self.model.group_id == group_id).values(responsible_id=responsible_id)
        await self.session.execute(stmt)
        await self.session.commit()

    @BaseDAO.with_exception
    async def assign_pvz_to_group(self, group_id: int, pvz_ids: list[int]):
        """Привязывает пвз к указанной группе по ее ID"""

        stmt = update(self.model).where(self.model.id.in_(pvz_ids)).values(group_id=group_id)
        await self.session.execute(stmt)
        await self.session.commit()

    @BaseDAO.with_exception
    async def set_responsible_for_group(
        self,
        group_id: int,
        responsible_id: int,
    ):
        stmt = update(self.model).where(self.model.group_id == group_id).values(responsible_id=responsible_id)
        await self.session.execute(stmt)
