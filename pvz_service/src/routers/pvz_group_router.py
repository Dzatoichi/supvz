from fastapi import APIRouter, Depends, Query

from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_group_schemas import (
    PVZGroupCreate,
    PVZGroupResponse,
    PVZGroupUpdate,
)
from src.schemas.pvz_schemas import PVZRead
from src.services.pvz_groups_service import PVZGroupsService
from src.utils.dependencies import (
    get_pvz_groups_repo,
    get_pvz_groups_service,
    get_pvzs_dao,
)

pvz_groups_router = APIRouter(prefix="/pvz_groups", tags=["PVZ_Groups"])


@pvz_groups_router.get("/all", response_model=list[PVZGroupResponse])
async def get_groups(
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Возвращает список всех групп ПВЗ."""

    groups = await service.get_groups(repo=repo)

    return groups


@pvz_groups_router.get("/pvzs", response_model=list[PVZRead])
async def get_pvzs_by_group(
    group_id: int | None = Query(default=None, description="ID группы"),
    group_name: str | None = Query(default=None, description="Имя группы"),
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    pvz_repo: PVZsDAO = Depends(get_pvzs_dao),
    group_repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Возвращает список ПВЗ по ID или имени группы."""

    pvzs = await service.get_pvzs_by_group(
        group_id=group_id,
        group_name=group_name,
        pvz_repo=pvz_repo,
        group_repo=group_repo,
    )
    return pvzs


@pvz_groups_router.get("")
async def get_groups_filtered(
    owner_id: int | None = Query(default=None, description="ID владельца"),
    curator_id: int | None = Query(default=None, description="ID куратора"),
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Возвращает список групп по owner_id или curator_id."""

    params_in = {"owner_id": owner_id, "curator_id": curator_id}
    return await service.get_groups_by_id(params=params_in, repo=repo)


@pvz_groups_router.post("", response_model=PVZGroupResponse)
async def create_group(
    data: PVZGroupCreate,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Создаёт новую группу ПВЗ."""

    return await service.create_group(data, repo)


@pvz_groups_router.patch("/{group_id}", response_model=PVZGroupResponse)
async def update_group(
    group_id: int,
    data: PVZGroupUpdate,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Обновляет существующую группу ПВЗ."""

    return await service.update_group(group_id, data, repo)


@pvz_groups_router.get("/{group_id}", response_model=PVZGroupResponse)
async def get_group(
    group_id: int,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Возвращает одну группу ПВЗ по ID."""

    group = await service.get_group_with_pvzs(group_id=group_id, repo=repo)

    return group


@pvz_groups_router.delete("/{group_id}", status_code=204)
async def delete_group(
    group_id: int,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
    pvz_repo: PVZsDAO = Depends(get_pvzs_dao),
):
    """Удаляет группу ПВЗ и отвязывает все её ПВЗ."""

    await service.delete_group(group_id=group_id, repo=repo, pvz_repo=pvz_repo)
