from fastapi import APIRouter, Depends, Query, status

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.employees_schemas import (
    EmployeeCreateRequestSchema,
    EmployeeResponseSchema,
    EmployeeUpdateRequestSchema,
    TransferRequestSchema,
)
from src.services.employees_service import EmployeesService
from src.utils.dependencies import (
    get_employees_repo,
    get_employees_service,
    get_pvz_repo,
)

employees_router = APIRouter(prefix="/employees", tags=["Employees"])


@employees_router.get("")
async def get_employees(
    user_id: int | None = Query(default=None, description="ID пользователя"),
    owner_id: int | None = Query(default=None, description="ID владельца"),
    employee_service: EmployeesService = Depends(get_employees_service),
    repo: EmployeesDAO = Depends(get_employees_repo),
):
    """
    Возвращает одного сотрудника по user_id, а также всех по owner_id.
    Можно передать только один параметр — либо user_id, либо owner_id.
    """

    params_in = {"user_id": user_id, "owner_id": owner_id}

    return await employee_service.get_employees_by_id(params=params_in, repo=repo)


@employees_router.post(
    "",
    response_model=EmployeeResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    payload: EmployeeCreateRequestSchema,
    employee_service: EmployeesService = Depends(get_employees_service),
    repo: EmployeesDAO = Depends(get_employees_repo),
):
    """Создаёт нового сотрудника."""

    employee = await employee_service.create_employee(data=payload, repo=repo)
    return employee


@employees_router.patch(
    "/{user_id}",
    response_model=EmployeeResponseSchema,
)
async def update_employee(
    user_id: int,
    payload: EmployeeUpdateRequestSchema,
    employee_service: EmployeesService = Depends(get_employees_service),
    repo: EmployeesDAO = Depends(get_employees_repo),
):
    """Обновляет данные сотрудника по его идентификатору."""

    updated_employee = await employee_service.update_employee(
        user_id=user_id,
        data=payload,
        repo=repo,
    )

    return updated_employee


@employees_router.post(
    "/{user_id}/assign",
    response_model=EmployeeResponseSchema,
)
async def assign_employee_to_pvz(
    user_id: int,
    pvz_in: TransferRequestSchema,
    employee_service: EmployeesService = Depends(get_employees_service),
    employees_repo: EmployeesDAO = Depends(get_employees_repo),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
):
    """Переводит сотрудника в другой ПВЗ."""

    return await employee_service.assign_employee_to_other_pvz(
        user_id=user_id,
        new_pvz_id=pvz_in.new_pvz_id,
        employees_repo=employees_repo,
        pvz_repo=pvz_repo,
    )


@employees_router.delete(
    "/{user_id}/unassign/{pvz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unassign_employee_from_pvz(
    user_id: int,
    pvz_id: int,
    employee_service: EmployeesService = Depends(get_employees_service),
    employees_repo: EmployeesDAO = Depends(get_employees_repo),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
):
    """Отвязывает сотрудника от ПВЗ, убирая назначение."""

    return await employee_service.unassign_employee_from_pvz(
        user_id=user_id,
        pvz_id=pvz_id,
        employees_repo=employees_repo,
        pvz_repo=pvz_repo,
    )


@employees_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
    user_id: int,
    repo: EmployeesDAO = Depends(get_employees_repo),
    employee_service: EmployeesService = Depends(get_employees_service),
):
    """Удаляет сотрудника по его user_id."""

    await employee_service.delete_employee(user_id=user_id, repo=repo)
