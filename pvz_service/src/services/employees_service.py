from fastapi import HTTPException, status
from sqlalchemy import or_

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.employees_schemas import (
    EmployeeCreateRequestSchema,
    EmployeeResponseSchema,
    EmployeeUpdateRequestSchema,
)


class EmployeesService:
    """
    Сервис для работы с сотрудниками и их привязкой к ПВЗ.
    """

    async def create_employee(
        self,
        data: EmployeeCreateRequestSchema,
        repo: EmployeesDAO,
    ) -> EmployeeResponseSchema:
        """Создаёт нового сотрудника."""
        condition = or_(
            repo.model.user_id == data.user_id,
            repo.model.phone_number == data.phone_number,
        )

        existing = await repo.get_employee(condition)

        if existing:
            if existing.user_id == data.user_id:
                message = "Employee with this user_id already exists"
            elif existing.phone_number == data.phone_number:
                message = "Employee with this phone number already exists"
            else:
                message = "Employee already exists"

            raise HTTPException(status.HTTP_409_CONFLICT, message)

        payload = {
            "user_id": data.user_id,
            "owner_id": data.owner_id,
            "phone_number": data.phone_number,
            "name": data.name,
            "pvzs": [],
        }

        new_employee = await repo.create(payload)

        return EmployeeResponseSchema.model_validate(new_employee)

    async def get_employees_by_id(
        self,
        params: dict,
        repo: EmployeesDAO,
    ) -> list[EmployeeResponseSchema] | EmployeeResponseSchema:
        """Возвращает сотрудника(ов) по ID."""

        actual_params = {k: v for k, v in params.items() if v is not None}

        if len(actual_params) == 0:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Нужно указать хотя бы один параметр (user_id или owner_id).",
            )

        if len(actual_params) > 1:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Используйте только один параметр для поиска.",
            )

        field_name, field_value = next(iter(actual_params.items()))

        employees = await repo.get_employees(**{field_name: field_value})

        if not employees:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Сотрудники не найдены",
            )

        if field_name == "user_id":
            return EmployeeResponseSchema.model_validate(employees[0])

        return [EmployeeResponseSchema.model_validate(emp) for emp in employees]

    async def update_employee(
        self,
        user_id: int,
        data: EmployeeUpdateRequestSchema,
        repo: EmployeesDAO,
    ) -> EmployeeResponseSchema:
        """Обновляет данные сотрудника."""
        update_data = data.model_dump(exclude_unset=True)
        updated_employee = await repo.update(user_id, **update_data)

        if not updated_employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        return EmployeeResponseSchema.model_validate(updated_employee)

    async def delete_employee(
        self,
        user_id: int,
        repo: EmployeesDAO,
    ) -> None:
        """Удаляет сотрудника и возвращает его данные."""
        user = await repo.get_employee(user_id=user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")

        success = await repo.delete(user_id=user_id)
        if not success:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete employee")

    async def assign_employee_to_other_pvz(
        self,
        user_id: int,
        new_pvz_id: int,
        employees_repo: EmployeesDAO,
        pvz_repo: PVZsDAO,
    ) -> EmployeeResponseSchema:
        """Добавляет сотруднику ещё один ПВЗ."""
        employee = await employees_repo.get_employee(user_id=user_id)
        if not employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")

        pvz = await pvz_repo.get_pvz(id=new_pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "PVZ not found")

        if pvz not in employee.pvzs:
            updated = await employees_repo.assign_to_pvz(user_id, pvz.id)
            return EmployeeResponseSchema.model_validate(updated)

        return EmployeeResponseSchema.model_validate(employee)

    async def unassign_employee_from_pvz(
        self,
        user_id: int,
        pvz_id: int,
        employees_repo: EmployeesDAO,
        pvz_repo: PVZsDAO,
    ) -> EmployeeResponseSchema:
        """Удаляет связь между сотрудником и конкретным ПВЗ."""
        employee = await employees_repo.get_employee(user_id=user_id)
        if not employee:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")

        pvz = await pvz_repo.get_pvz(id=pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "PVZ not found")

        if pvz in employee.pvzs:
            updated = await employees_repo.unassign_from_pvz(user_id, pvz.id)
            return EmployeeResponseSchema.model_validate(updated)

        return EmployeeResponseSchema.model_validate(employee)
