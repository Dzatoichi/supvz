from fastapi import APIRouter, Depends, Query, status

from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_group_schemas import (
    PVZGroupCreateSchema,
    PVZGroupResponseSchema,
    PVZGroupUpdateSchema,
)
from src.services.pvz_groups_service import PVZGroupsService
from src.services.pvz_service import PVZService
from src.utils.dependencies import (
    CurrentUserDep,
    get_pvz_groups_service,
    get_pvz_repo,
    get_pvz_service,
)

pvz_groups_router = APIRouter(prefix="/pvz_groups", tags=["PVZ_Groups"])


@pvz_groups_router.get("", response_model=list[PVZGroupResponseSchema])
async def get_groups(
    current_user: CurrentUserDep,
    responsible_id: int | None = Query(default=None, description="ID куратора"),
    service: PVZGroupsService = Depends(get_pvz_groups_service),
):
    """Возвращает список групп по owner_id или responsible_id."""

    return await service.get_groups(
        responsible_id=responsible_id,
        current_user_id=current_user.id,
    )


@pvz_groups_router.post("", response_model=PVZGroupResponseSchema)
async def create_group(
    data: PVZGroupCreateSchema,
    current_user: CurrentUserDep,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
):
    """Создаёт новую группу ПВЗ."""

    return await service.create_group(
        data=data,
        current_user_id=current_user.id,
    )


@pvz_groups_router.patch(
    "/{group_id}/responsible",
    status_code=status.HTTP_200_OK,
)
async def assign_responsible_to_group(
    group_id: int,
    responsible_id: int,
    current_user: CurrentUserDep,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
):
    """Назначение куратора для группы и всех ПВЗ в этой группе."""

    return await service.assign_responsible(
        group_id=group_id,
        responsible_id=responsible_id,
        current_user_id=current_user.id,
    )


@pvz_groups_router.patch("/{group_id}", response_model=PVZGroupResponseSchema)
async def update_group(
    group_id: int,
    current_user: CurrentUserDep,
    data: PVZGroupUpdateSchema,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
):
    """Обновляет существующую группу ПВЗ."""

    return await service.update_group(
        group_id=group_id,
        data=data,
        current_user_id=current_user.id,
    )


@pvz_groups_router.get("/{group_id}", response_model=PVZGroupResponseSchema)
async def get_group(
    group_id: int,
    current_user: CurrentUserDep,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
):
    """Возвращает одну группу ПВЗ по ID."""

    group = await service.get_group_with_pvzs(
        group_id=group_id,
        current_user_id=current_user.id,
    )

    return group


@pvz_groups_router.delete("/{group_id}", status_code=204)
async def delete_group(
    group_id: int,
    current_user: CurrentUserDep,
    group_service: PVZGroupsService = Depends(get_pvz_groups_service),
    pvz_service: PVZService = Depends(get_pvz_service),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
):
    """Удаляет группу ПВЗ и отвязывает все её ПВЗ."""

    await pvz_service.unassign_all_pvz_from_group(group_id=group_id, pvz_repo=pvz_repo)
    await group_service.delete_group(
        group_id=group_id,
        current_user_id=current_user.id,
    )
