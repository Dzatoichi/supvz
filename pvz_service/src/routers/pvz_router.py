from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.employees_schemas import EmployeeResponseSchema
from src.schemas.pvz_group_schemas import PVZAssignmentSchema
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate
from src.services.pvz_service import PVZService
from src.utils.dependencies import (
    CurrentUserDep,
    get_employees_repo,
    get_pvz_groups_repo,
    get_pvz_repo,
    get_pvz_service,
)

pvz_router = APIRouter(prefix="/pvzs", tags=["pvzs"])


@pvz_router.post("/", response_model=PVZRead, status_code=status.HTTP_201_CREATED)
async def add_pvz(
    pvz_in: PVZAdd,
    current_user: CurrentUserDep,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
    group_repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    pvz = await pvz_service.add_pvz(
        data=pvz_in,
        current_user_id=current_user.id,
        repo=repo,
        group_repo=group_repo,
    )

    return pvz


@pvz_router.patch(
    "/group_assignment",
    status_code=status.HTTP_200_OK,
)
async def assign_pvz_to_group(
    data: PVZAssignmentSchema,
    current_user: CurrentUserDep,
    service: PVZService = Depends(get_pvz_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
):
    """Привязка одного или нескольких ПВЗ к указанной группе."""

    return await service.assign_pvz_to_group(
        group_id=data.group_id,
        current_user_id=current_user.id,
        pvz_ids=data.pvz_ids,
        repo=repo,
        pvz_repo=pvz_repo,
    )


@pvz_router.patch("/{pvz_id}", response_model=PVZRead)
async def update_pvz_by_id(
    pvz_id: int,
    current_user: CurrentUserDep,
    pvz_in: PVZUpdate,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
    group_repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Обновляет данные существующего ПВЗ по его идентификатору."""

    pvz = await pvz_service.update_pvz_by_id(
        pvz_id=pvz_id,
        current_user_id=current_user.id,
        data=pvz_in,
        repo=repo,
        group_repo=group_repo,
    )
    return pvz


@pvz_router.get("/{pvz_id}", response_model=PVZRead)
async def get_pvz_by_id(
    pvz_id: int,
    current_user: CurrentUserDep,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Возвращает информацию о конкретном ПВЗ по его идентификатору."""

    pvz = await pvz_service.get_pvz_by_id(
        pvz_id=pvz_id,
        current_user_id=current_user.id,
        repo=repo,
    )
    return pvz


@pvz_router.get("/", response_model=Page[PVZRead])
async def get_pvzs(
    current_user: CurrentUserDep,
    code: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    group_id: Optional[int] = Query(None),
    repo: PVZsDAO = Depends(get_pvz_repo),
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
        repo=repo,
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
    repo: EmployeesDAO = Depends(get_employees_repo),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
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
        repo=repo,
        pvz_repo=pvz_repo,
        params=params,
    )


@pvz_router.delete("/{pvz_id}", response_model=PVZRead)
async def delete_pvz_by_id(
    pvz_id: int,
    current_user: CurrentUserDep,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Удаляет ПВЗ по его идентификатору."""

    result = await pvz_service.delete_pvz_by_id(
        pvz_id=pvz_id,
        current_user_id=current_user.id,
        repo=repo,
    )
    return result
