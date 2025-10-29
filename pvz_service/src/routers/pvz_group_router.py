from fastapi import APIRouter, Depends, Query, status

from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_group_schemas import (
    AssignPVZToGroupSchema,
    PVZGroupCreateSchema,
    PVZGroupResponseSchema,
    PVZGroupUpdateSchema,
)
from src.services.pvz_groups_service import PVZGroupsService
from src.utils.dependencies import (
    get_pvz_groups_repo,
    get_pvz_groups_service,
    get_pvzs_dao,
)

pvz_groups_router = APIRouter(prefix="/pvz_groups", tags=["PVZ_Groups"])


@pvz_groups_router.get("", response_model=list[PVZGroupResponseSchema])
async def get_groups(
    owner_id: int | None = Query(default=None, description="ID владельца"),
    curator_id: int | None = Query(default=None, description="ID куратора"),
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Возвращает список групп по owner_id или curator_id."""

    params_in = {"owner_id": owner_id, "curator_id": curator_id}
    return await service.get_groups(params=params_in, repo=repo)


@pvz_groups_router.post("", response_model=PVZGroupResponseSchema)
async def create_group(
    data: PVZGroupCreateSchema,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Создаёт новую группу ПВЗ."""

    return await service.create_group(data, repo)


@pvz_groups_router.post(
    "/{group_id}/assign-pvz",
    status_code=status.HTTP_200_OK,
)
async def assign_pvz_to_group(
    group_id: int,
    data: AssignPVZToGroupSchema,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
    pvz_repo: PVZsDAO = Depends(get_pvzs_dao),
):
    """Привязка одного или нескольких ПВЗ к указанной группе."""

    return await service.assign_pvz_to_group(
        group_id=group_id,
        pvz_ids=data.pvz_ids,
        repo=repo,
        pvz_repo=pvz_repo,
    )


@pvz_groups_router.post(
    "/{group_id}/assign-curator/{curator_id}",
    status_code=status.HTTP_200_OK,
)
async def assign_curator_to_group(
    group_id: int,
    curator_id: int,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Назначение куратора для группы и всех ПВЗ в этой группе."""

    return await service.assign_curator(group_id, curator_id, repo)


@pvz_groups_router.patch("/{group_id}", response_model=PVZGroupResponseSchema)
async def update_group(
    group_id: int,
    data: PVZGroupUpdateSchema,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    """Обновляет существующую группу ПВЗ."""

    return await service.update_group(group_id, data, repo)


@pvz_groups_router.get("/{group_id}", response_model=PVZGroupResponseSchema)
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
