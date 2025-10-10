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

    async def get_employees_by_pvz_id(self, pvz_id: int):
        async with self._get_session() as session:
            result = await session.execute(select(self.model).join(self.model.pvzs).where(PVZs.id == pvz_id))
            return result.scalars().all()

    async def get_pvz_by_id(self, pvz_id: int) -> PVZs | None:
        """Вспомогательный метод для сервисов, чтобы доставать Pvz."""

        async with self._get_session() as session:
            return await session.get(PVZs, pvz_id)

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
