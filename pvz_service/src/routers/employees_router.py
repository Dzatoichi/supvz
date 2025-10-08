from fastapi import APIRouter, Depends

from src.schemas.employees_schemas import TransferRequest
from src.services.employees_service import EmployeesService
from src.utils.dependencies import get_employees_service

employees_router = APIRouter(prefix="/employees", tags=["employees"])


@employees_router.get("/{pvz_id}")
async def get_employees(
    pvz_id: int,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    return await employee_service.get_employees_by_pvz(pvz_id)


@employees_router.post("/{employee_id}/assign")
async def assign_employee_to_other_pvz(
    employee_id: int,
    pvz_in: TransferRequest,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    return await employee_service.assign_employee_to_other_pvz(employee_id, pvz_in.new_pvz_id)


@employees_router.delete("/{employee_id}/unassign/{pvz_id}")
async def unassign_employee_to_pvz(
    employee_id: int,
    pvz_id: int,
    employee_service: EmployeesService = Depends(get_employees_service),
):
    return await employee_service.unassign_employee_to_pvz(employee_id, pvz_id)
