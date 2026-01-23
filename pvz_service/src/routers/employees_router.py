from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.schemas.employees_schemas import (
    EmployeeCreateRequestSchema,
    EmployeeResponseSchema,
    EmployeeUpdateRequestSchema,
    TransferRequestSchema,
)
from src.services.employees_service import EmployeesService
from src.utils.dependencies import (
    CurrentUserDep,
    InternalKeyDep,
    get_employees_service,
)

employees_router = APIRouter(prefix="/employees", tags=["Employees"])


@employees_router.get("/{user_id}", response_model=EmployeeResponseSchema)
async def get_employee(
    user_id: int,
    current_user: CurrentUserDep,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    """Возвращает одного сотрудника по его user_id."""
    return await employee_service.get_employee_by_user_id(
        user_id=user_id,
        current_user_id=current_user.id,
    )


@employees_router.get("", response_model=Page[EmployeeResponseSchema])
async def get_employees(
    current_user: CurrentUserDep,
    pvz_id: int | None = Query(default=None, description="ID ПВЗ для фильтрации сотрудников"),
    employee_service: EmployeesService = Depends(get_employees_service),
    params: Params = Depends(),
):
    """
    Возвращает всех сотрудников указанного владельца.
    Можно также указать ID ПВЗ для фильтрации сотрудников конкретного ПВЗ.
    """
    return await employee_service.get_employees_filtered(
        current_user_id=current_user.id,
        pvz_id=pvz_id,
        params=params,
    )


@employees_router.post(
    "",
    response_model=EmployeeResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    payload: EmployeeCreateRequestSchema,
    _: None = InternalKeyDep,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    """Создаёт нового сотрудника."""

    employee = await employee_service.create_employee(data=payload)
    return employee


@employees_router.patch(
    "/{user_id}",
    response_model=EmployeeResponseSchema,
)
async def update_employee(
    user_id: int,
    payload: EmployeeUpdateRequestSchema,
    current_user: CurrentUserDep,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    """Обновляет данные сотрудника по его идентификатору."""

    updated_employee = await employee_service.update_employee(
        user_id=user_id,
        data=payload,
        current_user_id=current_user.id,
    )

    return updated_employee


@employees_router.post(
    "/{user_id}/assign",
    response_model=EmployeeResponseSchema,
)
async def assign_employee_to_pvz(
    user_id: int,
    current_user: CurrentUserDep,
    pvz_in: TransferRequestSchema,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    """Переводит сотрудника в другой ПВЗ."""

    return await employee_service.assign_employee_to_other_pvz(
        user_id=user_id,
        current_user_id=current_user.id,
        new_pvz_id=pvz_in.new_pvz_id,
    )


@employees_router.delete(
    "/{user_id}/unassign/{pvz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unassign_employee_from_pvz(
    user_id: int,
    pvz_id: int,
    current_user: CurrentUserDep,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    """Отвязывает сотрудника от ПВЗ, убирая назначение."""

    return await employee_service.unassign_employee_from_pvz(
        user_id=user_id,
        current_user_id=current_user.id,
        pvz_id=pvz_id,
    )


@employees_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
    user_id: int,
    current_user: CurrentUserDep,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    """Удаляет сотрудника по его user_id."""

    await employee_service.delete_employee(
        user_id=user_id,
        current_user_id=current_user.id,
    )
