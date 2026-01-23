from typing import Optional

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.employees.employees import Employees
from src.models.pvzs.PVZs import PVZs


class EmployeesDAO(BaseDAO[Employees]):
    """
    Класс, наследующий базовый DAO для работы с сущностями сотрудника.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(model=Employees, session=session)

    @BaseDAO.with_exception
    async def get_employee(self, *args, **kwargs) -> Optional[Employees]:
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
    async def get_employees(self, *args, **kwargs) -> Optional[list[Employees]]:
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
        return result.scalars().all()

    @BaseDAO.with_exception
    async def assign_to_pvz(self, user_id: int, pvz_id: int):
        """Привязывает сотрудника к пункту выдачи заказов (ПВЗ)."""
        employee = await self.session.get(Employees, user_id)
        pvz = await self.session.get(PVZs, pvz_id)
        if pvz not in employee.pvzs:
            employee.pvzs.append(pvz)
            await self.session.commit()
            await self.session.refresh(employee)
        return employee

    @BaseDAO.with_exception
    async def unassign_from_pvz(self, employee_id: int, pvz_id: int):
        """Отвязывает сотрудника от пункта выдачи заказов (ПВЗ)."""
        employee = await self.session.get(Employees, employee_id)
        pvz = await self.session.get(PVZs, pvz_id)
        if pvz in employee.pvzs:
            employee.pvzs.remove(pvz)
            await self.session.commit()
            await self.session.refresh(employee)
        return employee

    @BaseDAO.with_exception
    async def update(self, user_id: int, **kwargs):
        """Обновляет данные сотрудника по его user_id."""
        stmt = update(self.model).where(self.model.user_id == user_id).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        updated = result.scalar_one_or_none()
        return updated

    @BaseDAO.with_exception
    async def get_employees_filtered(
        self,
        owner_id: int,
        params: Params,
        pvz_id: int | None = None,
        position_id: int | None = None,
    ) -> Employees:
        """Возвращает список сотрудников владельца, при необходимости фильтрует по ID ПВЗ."""
        stmt = select(self.model).where(self.model.owner_id == owner_id)
        if pvz_id is not None:
            stmt = stmt.where(self.model.pvzs.any(id=pvz_id))
        if position_id is not None:
            stmt = stmt.where(self.model.position_id == position_id)
        # apaginate добавит LIMIT и OFFSET прямо в SQL-запрос
        return await apaginate(self.session, stmt, params=params)
