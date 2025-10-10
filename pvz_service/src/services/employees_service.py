from fastapi import HTTPException, status

from src.dao.employeesDAO import EmployeesDAO
from src.models.employees.employees import Employees
from src.schemas.employees_schemas import EmployeeResponse


class EmployeesService:
    """
    Сервис для работы с сотрудниками и их привязкой к ПВЗ.
    """

    def __init__(self, repo: EmployeesDAO):
        self.repo = repo

    async def create_employee(self, payload: dict) -> EmployeeResponse:
        """Создаёт нового сотрудника."""

        employee = self.repo.get_by_id(payload["user_id"])
        if employee:
            raise HTTPException(status.HTTP_409_CONFLICT, "Employee already exists")

        new_employee = await self.repo.create(payload)

        return EmployeeResponse(
            id=new_employee.id,
            user_id=new_employee.user_id,
            owner_id=new_employee.owner_id,
            pvzs=new_employee.pvzs,
        )

    async def get_employee_by_id(self, employee_id: int) -> Employees | None:
        """Возвращает сотрудника по ID."""
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        return employee

    async def update_employee(self, employee_id: int, update_data: dict) -> Employees | None:
        """Обновляет данные сотрудника."""
        updated_employee = await self.repo.update(employee_id, **update_data)

        if not updated_employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        return updated_employee

    async def delete_employee(self, employee_id: int) -> bool:
        """Удаляет сотрудника."""
        deleted = await self.repo.delete(employee_id)

        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        return deleted

    async def get_employees_by_pvz(self, pvz_id: int) -> list[Employees]:
        """Возвращает список сотрудников, привязанных к заданному ПВЗ."""

        return await self.repo.get_employees_by_pvz_id(pvz_id)

    async def assign_employee_to_other_pvz(self, employee_id: int, new_pvz_id: int) -> Employees:
        """Добавляет сотруднику ещё один ПВЗ."""

        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Employee not found")

        pvz = await self.repo.get_pvz_by_id(new_pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Pvz not found")

        if pvz not in employee.pvzs:
            return await self.repo.assign_to_pvz(employee_id, pvz.id)

        return employee

    async def unassign_employee_to_pvz(self, employee_id: int, pvz_id: int) -> Employees:
        """Удаляет связь между сотрудником и конкретным ПВЗ."""

        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")

        pvz = await self.repo.get_pvz_by_id(pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pvz not found")

        if pvz in employee.pvzs:
            return await self.repo.unassign_from_pvz(employee_id, pvz.id)

        return employee
