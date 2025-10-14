from fastapi import HTTPException, status
from sqlalchemy import or_

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.employees_schemas import (
    EmployeeCreateRequest,
    EmployeeResponse,
    EmployeeUpdateRequest,
)


class EmployeesService:
    """
    Сервис для работы с сотрудниками и их привязкой к ПВЗ.
    """

    def __init__(self, repo: EmployeesDAO):
        self.repo = repo

    async def create_employee(self, payload: dict) -> EmployeeResponseSchema:
    async def create_employee(
        self,
        data: EmployeeCreateRequest,
        repo: EmployeesDAO,
    ) -> EmployeeResponse:
        """Создаёт нового сотрудника."""
        condition = or_(
            self.repo.model.user_id == payload["user_id"],
            self.repo.model.phone_number == payload.get("phone_number"),
        )

        existing = await self.repo.get_employee(condition)

        if existing:
            if existing.user_id == payload["user_id"]:
                message = "Employee with this user_id already exists"
            elif existing.phone_number == payload.get("phone_number"):
                message = "Employee with this phone number already exists"
            else:
                message = "Employee already exists"

            raise HTTPException(status.HTTP_409_CONFLICT, message)

        payload = {
            "user_id": data.user_id,
            "owner_id": data.owner_id,
            "pvzs": data.pvzs,
        }

        new_employee = await repo.create(payload)

        return EmployeeResponseSchema(
            id=new_employee.id,
            user_id=new_employee.user_id,
            owner_id=new_employee.owner_id,
            pvzs=new_employee.pvzs,
        )

    async def get_employee_by_id(
        self,
        user_id: int
        repo: EmployeesDAO,
    ) -> EmployeeResponse:
        """Возвращает сотрудника по ID."""
        employee = await repo.get_employee(user_id=user_id)
        if not employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        return EmployeeResponse(
            id=employee.id,
            user_id=employee.user_id,
            owner_id=employee.owner_id,
            pvzs=employee.pvzs,
        )

    async def update_employee(
        self,
        employee_id: int,
        data: EmployeeUpdateRequest,
        repo: EmployeesDAO,
    ) -> EmployeeResponse:
        """Обновляет данные сотрудника."""
        update_data = data.model_dump(exclude_unset=True)
        updated_employee = await repo.update(employee_id, **update_data)

        if not updated_employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        return EmployeeResponse(
            id=updated_employee.id,
            user_id=updated_employee.user_id,
            owner_id=updated_employee.owner_id,
            pvzs=updated_employee.pvzs,
        )

    async def delete_employee(
        self,
        user_id: int,
        repo: EmployeesDAO,
    ) -> EmployeeResponse:
        """Удаляет сотрудника и возвращает его данные."""
        user = await self.repo.get_employee(user_id=user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        user_info = EmployeeResponse(
            id=user.id,
            user_id=user.user_id,
            owner_id=user.owner_id,
            pvzs=user.pvzs,
        )

        success = await repo.delete(user_id)
        if not success:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete employee"
            )

        return user_info

    async def get_employees_by_pvz(
        self,
        pvz_id: int,
        repo: EmployeesDAO,
    ) -> list[EmployeeResponse]:
        """Возвращает список сотрудников, привязанных к заданному ПВЗ."""
        employees = await repo.get_employees_by_pvz_id(pvz_id)

        return [
            EmployeeResponse(
                id=e.id,
                user_id=e.user_id,
                owner_id=e.owner_id,
                pvzs=e.pvzs,
            )
            for e in employees
        ]

    async def assign_employee_to_other_pvz(
        self,
        employee_id: int,
        new_pvz_id: int,
        employees_repo: EmployeesDAO,
        pvz_repo: PVZsDAO,
    ) -> EmployeeResponse:
        """Добавляет сотруднику ещё один ПВЗ."""
        employee = await employees_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")

        pvz = await pvz_repo.get_pvz(id=new_pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "PVZ not found")

        if pvz not in employee.pvzs:
            updated = await employees_repo.assign_to_pvz(employee_id, pvz.id)
            return EmployeeResponse(
                id=updated.id,
                user_id=updated.user_id,
                owner_id=updated.owner_id,
                pvzs=updated.pvzs,
            )

        return EmployeeResponse(
            id=employee.id,
            user_id=employee.user_id,
            owner_id=employee.owner_id,
            pvzs=employee.pvzs,
        )

    async def unassign_employee_from_pvz(
        self,
        employee_id: int,
        pvz_id: int,
        employees_repo: EmployeesDAO,
        pvz_repo: PVZsDAO,
    ) -> EmployeeResponse:
        """Удаляет связь между сотрудником и конкретным ПВЗ."""
        employee = await employees_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")

        pvz = await pvz_repo.get_pvz(id=pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "PVZ not found")

        if pvz in employee.pvzs:
            updated = await employees_repo.unassign_from_pvz(employee_id, pvz.id)
            return EmployeeResponse(
                id=updated.id,
                user_id=updated.user_id,
                owner_id=updated.owner_id,
                pvzs=updated.pvzs,
            )

        return EmployeeResponse(
            id=employee.id,
            user_id=employee.user_id,
            owner_id=employee.owner_id,
            pvzs=employee.pvzs,
        )
