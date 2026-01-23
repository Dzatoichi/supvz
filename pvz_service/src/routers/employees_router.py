from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.enums.inbox import EventType
from src.schemas.employees_schemas import (
    EmployeeCreateRequestSchema,
    EmployeeResponseSchema,
    EmployeeUpdateRequestSchema,
    TransferRequestSchema,
)
from src.services.employees_service import EmployeesService
from src.services.inbox_service import InboxService
from src.utils.dependencies import (
    CurrentUserDep,
    IdempotencyKeyDep,
    InternalKeyDep,
    get_employees_service,
    get_inbox_service,
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
    event_id: IdempotencyKeyDep,
    _: None = InternalKeyDep,
    employee_service: EmployeesService = Depends(get_employees_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Создаёт нового сотрудника."""

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.CREATE_EMPLOYEE,
        payload=payload.model_dump(),
        handler=lambda: employee_service.create_employee(data=payload),
    )


@employees_router.patch(
    "/{user_id}",
    response_model=EmployeeResponseSchema,
)
async def update_employee(
    user_id: int,
    payload: EmployeeUpdateRequestSchema,
    event_id: IdempotencyKeyDep,
    current_user: CurrentUserDep,
    _: None = InternalKeyDep,
    employee_service: EmployeesService = Depends(get_employees_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.UPDATE_EMPLOYEE,
        payload={
            "user_id": user_id,
            **payload.model_dump(),
        },
        handler=lambda: employee_service.update_employee(
            user_id=user_id,
            data=payload,
            current_user_id=current_user.id,
        ),
    )


@employees_router.post(
    "/{user_id}/assign",
    response_model=EmployeeResponseSchema,
)
async def assign_employee_to_pvz(
    user_id: int,
    pvz_in: TransferRequestSchema,
    event_id: IdempotencyKeyDep,
    current_user: CurrentUserDep,
    _: None = InternalKeyDep,
    employee_service: EmployeesService = Depends(get_employees_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.ASSIGN_EMPLOYEE_TO_PVZ,
        payload={
            "user_id": user_id,
            **pvz_in.model_dump(),
        },
        handler=lambda: employee_service.assign_employee_to_other_pvz(
            user_id=user_id,
            current_user_id=current_user.id,
            new_pvz_id=pvz_in.new_pvz_id,
        ),
    )


@employees_router.delete(
    "/{user_id}/unassign/{pvz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unassign_employee_from_pvz(
    user_id: int,
    pvz_id: int,
    event_id: IdempotencyKeyDep,
    current_user: CurrentUserDep,
    _: None = InternalKeyDep,
    employee_service: EmployeesService = Depends(get_employees_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.UNASSIGN_EMPLOYEE_FROM_PVZ,
        payload={"user_id": user_id, "pvz_id": pvz_id},
        handler=lambda: employee_service.unassign_employee_from_pvz(
            user_id=user_id,
            current_user_id=current_user.id,
            pvz_id=pvz_id,
        ),
    )


@employees_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
    user_id: int,
    event_id: IdempotencyKeyDep,
    current_user: CurrentUserDep,
    _: None = InternalKeyDep,
    employee_service: EmployeesService = Depends(get_employees_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.DELETE_EMPLOYEE,
        payload={"user_id": user_id},
        handler=lambda: employee_service.delete_employee(
            user_id=user_id,
            current_user_id=current_user.id,
        ),
    )
