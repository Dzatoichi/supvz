from fastapi import APIRouter, Depends, status

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
    get_employees_service,
    get_employees_repo,
    get_pvz_repo,
)

employees_router = APIRouter(prefix="/employees", tags=["Employees"])


@employees_router.get(
    "/pvz/{pvz_id}",
    response_model=list[EmployeeResponseSchema],
)
async def get_employees(
    pvz_id: int,
    employee_service: EmployeesService = Depends(get_employees_service),
    repo: EmployeesDAO = Depends(get_employees_repo),
):
    return await employee_service.get_employees_by_pvz(pvz_id=pvz_id, repo=repo)


@employees_router.get(
    "/{employee_id}",
    response_model=EmployeeResponseSchema,
)
async def get_employee_by_id(
    employee_id: int,
    employee_service: EmployeesService = Depends(get_employees_service),
    repo: EmployeesDAO = Depends(get_employees_repo),
):
    employee = await employee_service.get_employee_by_id(
        employee_id=employee_id, repo=repo
    )

    return employee


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
    "/{employee_id}",
    response_model=EmployeeResponseSchema,
)
async def update_employee(
    employee_id: int,
    payload: EmployeeUpdateRequestSchema,
    employee_service: EmployeesService = Depends(get_employees_service),
    repo: EmployeesDAO = Depends(get_employees_repo),
):
    updated_employee = await employee_service.update_employee(
        employee_id=employee_id,
        data=payload,
        repo=repo,
    )

    return updated_employee


@employees_router.post(
    "/{employee_id}/assign",
    response_model=EmployeeResponseSchema,
)
async def assign_employee_to_pvz(
    employee_id: int,
    pvz_in: TransferRequestSchema,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    return await employee_service.assign_employee_to_other_pvz(
        employee_id=employee_id,
        new_pvz_id=pvz_in.new_pvz_id,
        employees_repo=employees_repo,
        pvz_repo=pvz_repo,
    )


@employees_router.delete(
    "/{employee_id}/unassign/{pvz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unassign_employee_from_pvz(
    employee_id: int,
    pvz_id: int,
    employee_service: EmployeesService = Depends(get_employees_service),
    employees_repo: EmployeesDAO = Depends(get_employees_repo),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
):
    return await employee_service.unassign_employee_from_pvz(
        employee_id=employee_id,
        pvz_id=pvz_id,
        employees_repo=employees_repo,
        pvz_repo=pvz_repo,
    )


@employees_router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
    employee_id: int,
    repo: EmployeesDAO = Depends(get_employees_repo),
    employee_service: EmployeesService = Depends(get_employees_service),
):
    await employee_service.delete_employee(employee_id=employee_id, repo=repo)

    return None
