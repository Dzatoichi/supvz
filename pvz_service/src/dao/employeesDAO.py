from typing import Optional

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, update

from src.dao.baseDAO import BaseDAO
from src.models.employees.employees import Employees
from src.models.pvzs.PVZs import PVZs


class EmployeesDAO(BaseDAO[Employees]):
    """
    Класс, наследующий базовый DAO для работы с сущностями сотрудника.
    """

    def __init__(self):
        super().__init__(model=Employees)

    @BaseDAO.with_exception
    async def get_employee(self, *args, **kwargs) -> Optional[Employees]:
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
    async def get_employees(self, *args, **kwargs) -> Optional[list[Employees]]:
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
    async def assign_to_pvz(self, employee_id: int, pvz_id: int):
        """Привязывает сотрудника к пункту выдачи заказов (ПВЗ)."""
        async with self._get_session() as session:
            employee = await session.get(Employees, employee_id)
            pvz = await session.get(PVZs, pvz_id)
            if pvz not in employee.pvzs:
                employee.pvzs.append(pvz)
                await session.commit()
                await session.refresh(employee)
            return employee

    @BaseDAO.with_exception
    async def unassign_from_pvz(self, employee_id: int, pvz_id: int):
        """Отвязывает сотрудника от пункта выдачи заказов (ПВЗ)."""
        async with self._get_session() as session:
            employee = await session.get(Employees, employee_id)
            pvz = await session.get(PVZs, pvz_id)
            if pvz in employee.pvzs:
                employee.pvzs.remove(pvz)
                await session.commit()
                await session.refresh(employee)
            return employee

    @BaseDAO.with_exception
    async def update(self, user_id: int, **kwargs):
        """Обновляет данные сотрудника по его user_id."""
        async with self._get_session() as session:
            stmt = update(self.model).where(self.model.user_id == user_id).values(**kwargs).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()
            updated = result.scalar_one_or_none()
            if updated:
                await session.refresh(updated)
            return updated

    @BaseDAO.with_exception
    async def get_employees_filtered(
        self, user_id: int, params: Params, pvz_id: int | None = None, position_id: int | None = None
    ) -> Employees:
        """Возвращает список сотрудников владельца, при необходимости фильтрует по ID ПВЗ."""
        async with self._get_session() as session:
            stmt = select(self.model).where(self.model.owner_id == user_id)
            if pvz_id is not None:
                stmt = stmt.where(self.model.pvzs.any(id=pvz_id))
            if position_id is not None:
                stmt = stmt.where(self.model.position_id == position_id)
            # paginate добавит LIMIT и OFFSET прямо в SQL-запрос
            return await paginate(session, stmt, params=params)
