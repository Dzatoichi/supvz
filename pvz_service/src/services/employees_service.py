from fastapi_pagination import Params
from sqlalchemy import or_

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.employees_schemas import (
    EmployeeCreateRequestSchema,
    EmployeeResponseSchema,
    EmployeeUpdateRequestSchema,
)
from src.utils.exceptions import (
    EmployeeAlreadyExistsException,
    EmployeeNotFoundException,
    PVZAlreadyExistsException,
    PVZNotFoundException,
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
                raise EmployeeAlreadyExistsException("Сотрудник с таким user_id уже существует.")
            elif existing.phone_number == data.phone_number:
                raise EmployeeAlreadyExistsException("Сотрудник с таким номером телефона уже существует.")
            else:
                raise EmployeeAlreadyExistsException("Такой сотрудник уже существует.")

        payload = {
            "user_id": data.user_id,
            "owner_id": data.owner_id,
            "position_id": data.position_id,
            "position_source": data.position_source,
            "phone_number": data.phone_number,
            "name": data.name,
            "pvzs": [],
        }

        new_employee = await repo.create(payload)

        return EmployeeResponseSchema.model_validate(new_employee)

    async def get_employee_by_user_id(
        self,
        user_id: int,
        repo: EmployeesDAO,
    ) -> EmployeeResponseSchema:
        """Возвращает одного сотрудника по user_id."""
        employee = await repo.get_employee(user_id=user_id)

        if not employee:
            raise EmployeeNotFoundException("Сотрудник не найден.")

        return EmployeeResponseSchema.model_validate(employee)

    async def get_employees_filtered(
        self,
        owner_id: int,
        pvz_id: int | None,
        position_id: int | None,
        repo: EmployeesDAO,
        params: Params,
    ) -> list[EmployeeResponseSchema]:
        """Возвращает список сотрудников владельца, при необходимости фильтрует по ПВЗ."""
        employees = await repo.get_employees_filtered(
            user_id=owner_id,
            pvz_id=pvz_id,
            position_id=position_id,
            params=params,
        )

        if not employees:
            raise EmployeeNotFoundException("Сотрудники не найдены.")
        employees.items = [EmployeeResponseSchema.model_validate(emp) for emp in employees.items]

        return employees

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
            raise EmployeeNotFoundException("Сотрудник не найден.")

        return EmployeeResponseSchema.model_validate(updated_employee)

    async def delete_employee(
        self,
        user_id: int,
        repo: EmployeesDAO,
    ) -> None:
        """Удаляет сотрудника и возвращает его данные."""
        user = await repo.get_employee(user_id=user_id)

        if not user:
            raise EmployeeNotFoundException("Сотрудник не найден.")

        await repo.delete(user_id=user_id)

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
            raise EmployeeNotFoundException("Сотрудник не найден.")

        pvz = await pvz_repo.get_pvz(id=new_pvz_id)
        if not pvz:
            raise PVZNotFoundException("ПВЗ не найден.")

        if pvz in employee.pvzs:
            raise PVZAlreadyExistsException("Сотрудник уже привязан к этому пвз.")

        updated = await employees_repo.assign_to_pvz(user_id, pvz.id)
        return EmployeeResponseSchema.model_validate(updated)

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
            raise EmployeeNotFoundException("Сотрудник не найден")

        pvz = await pvz_repo.get_pvz(id=pvz_id)
        if not pvz:
            raise PVZNotFoundException("ПВЗ не найден.")

        updated = await employees_repo.unassign_from_pvz(user_id, pvz.id)
        return EmployeeResponseSchema.model_validate(updated)
