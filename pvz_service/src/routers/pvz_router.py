from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.enums.inbox import EventType
from src.schemas.employees_schemas import EmployeeResponseSchema
from src.schemas.pvz_group_schemas import PVZAssignmentSchema
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate
from src.services.inbox_service import InboxService
from src.services.pvz_service import PVZService
from src.utils.dependencies import (
    CurrentUserDep,
    IdempotencyKeyDep,
    InternalKeyDep,
    get_inbox_service,
    get_pvz_service,
)

pvz_router = APIRouter(prefix="/pvzs", tags=["pvzs"])


@pvz_router.post(
    "",
    response_model=PVZRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_pvz(
    pvz_in: PVZAdd,
    event_id: IdempotencyKeyDep,
    current_user: CurrentUserDep,
    _: None = InternalKeyDep,
    pvz_service: PVZService = Depends(get_pvz_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.CREATE_PVZ,
        payload=pvz_in.model_dump(mode="json"),
        handler=lambda: pvz_service.add_pvz(
            data=pvz_in,
            current_user_id=current_user.id,
        ),
    )


@pvz_router.patch(
    "/group_assignment",
    status_code=status.HTTP_200_OK,
)
async def assign_pvz_to_group(
    data: PVZAssignmentSchema,
    current_user: CurrentUserDep,
    event_id: IdempotencyKeyDep,
    _: None = InternalKeyDep,
    service: PVZService = Depends(get_pvz_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Привязка одного или нескольких ПВЗ к указанной группе."""

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.ASSIGN_PVZ_TO_GROUP,
        payload=data.model_dump(mode="json"),
        handler=lambda: service.assign_pvz_to_group(
            group_id=data.group_id,
            current_user_id=current_user.id,
            pvz_ids=data.pvz_ids,
        ),
    )


@pvz_router.patch("/{pvz_id}", response_model=PVZRead)
async def update_pvz_by_id(
    pvz_id: int,
    current_user: CurrentUserDep,
    pvz_in: PVZUpdate,
    event_id: IdempotencyKeyDep,
    _: None = InternalKeyDep,
    pvz_service: PVZService = Depends(get_pvz_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Обновляет данные существующего ПВЗ по его идентификатору."""

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.UPDATE_PVZ,
        payload=pvz_in.model_dump(mode="json"),
        handler=lambda: pvz_service.update_pvz_by_id(
            pvz_id=pvz_id,
            current_user_id=current_user.id,
            data=pvz_in,
        ),
    )


@pvz_router.get("/{pvz_id}", response_model=PVZRead)
async def get_pvz_by_id(
    pvz_id: int,
    current_user: CurrentUserDep,
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Возвращает информацию о конкретном ПВЗ по его идентификатору."""

    pvz = await pvz_service.get_pvz_by_id(
        pvz_id=pvz_id,
        current_user_id=current_user.id,
    )
    return pvz


@pvz_router.get("", response_model=Page[PVZRead])
async def get_pvzs(
    current_user: CurrentUserDep,
    code: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    group_id: Optional[int] = Query(None),
    pvz_service: PVZService = Depends(get_pvz_service),
    params: Params = Depends(),
):
    """Возвращает список всех ПВЗ с возможностью фильтрации по коду, типу, адресу или группе."""

    pvzs = await pvz_service.get_pvzs(
        current_user_id=current_user.id,
        code=code,
        type=type,
        address=address,
        group_id=group_id,
        params=params,
    )
    return pvzs


@pvz_router.get(
    "/{pvz_id}/employees",
    response_model=Page[EmployeeResponseSchema],
)
async def get_employees_by_pvz(
    pvz_id: int,
    current_user: CurrentUserDep,
    pvz_service: PVZService = Depends(get_pvz_service),
    params: Params = Depends(),
):
    """
    Возвращает список сотрудников, работающих в указанном ПВЗ.

    Доступ разрешен только сотрудникам, которые сами привязаны к этому ПВЗ.
    Проверяется, что pvz_id содержится в списке ПВЗ пользователя.
    """
    return await pvz_service.get_employees_by_pvz_checked(
        user_id=current_user.id,
        pvz_id=pvz_id,
        params=params,
    )


@pvz_router.delete("/{pvz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pvz_by_id(
    pvz_id: int,
    current_user: CurrentUserDep,
    event_id: IdempotencyKeyDep,
    _: None = InternalKeyDep,
    pvz_service: PVZService = Depends(get_pvz_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Удаляет ПВЗ по его идентификатору."""

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.DELETE_PVZ,
        payload={"pvz_id": pvz_id},
        handler=lambda: pvz_service.delete_pvz_by_id(
            pvz_id=pvz_id,
            current_user_id=current_user.id,
        ),
    )
