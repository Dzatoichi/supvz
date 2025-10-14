from typing import Optional

from sqlalchemy import select

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
    async def get_pvz_by_id(self, pvz_id: int) -> PVZs | None:
        """Вспомогательный метод для сервисов, чтобы доставать Pvz."""

        async with self._get_session() as session:
            return await session.get(PVZs, pvz_id)

    @BaseDAO.with_exception
    async def assign_to_pvz(self, employee_id: int, pvz_id: int):
        async with self._get_session() as session:
            employee = await session.get(Employees, employee_id)
            pvz = await session.get(PVZs, pvz_id)
            if pvz not in employee.pvzs:
                employee.pvzs.append(pvz)
                await session.commit()
                await session.refresh(employee)
            return employee

    async def unassign_from_pvz(self, employee_id: int, pvz_id: int):
        async with self._get_session() as session:
            employee = await session.get(Employees, employee_id)
            pvz = await session.get(PVZs, pvz_id)
            if pvz in employee.pvzs:
                employee.pvzs.remove(pvz)
                await session.commit()
                await session.refresh(employee)
            return employee
