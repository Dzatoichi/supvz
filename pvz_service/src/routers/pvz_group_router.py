from fastapi import APIRouter, Depends, Query, status

from src.enums.inbox import EventType
from src.schemas.pvz_group_schemas import (
    PVZGroupCreateSchema,
    PVZGroupResponseSchema,
    PVZGroupUpdateSchema,
)
from src.services.inbox_service import InboxService
from src.services.pvz_groups_service import PVZGroupsService
from src.services.pvz_service import PVZService
from src.utils.dependencies import (
    CurrentUserDep,
    IdempotencyKeyDep,
    get_inbox_service,
    get_pvz_groups_service,
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
    event_id: IdempotencyKeyDep,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Создаёт новую группу ПВЗ."""

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.CREATE_PVZ_GROUP,
        payload=data.model_dump(mode="json"),
        handler=lambda: service.create_group(
            data=data,
            current_user_id=current_user.id,
        ),
    )


@pvz_groups_router.patch(
    "/{group_id}/responsible",
    status_code=status.HTTP_200_OK,
)
async def assign_responsible_to_group(
    group_id: int,
    responsible_id: int,
    current_user: CurrentUserDep,
    event_id: IdempotencyKeyDep,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Назначение куратора для группы и всех ПВЗ в этой группе."""

    payload_data = {"group_id": group_id, "responsible_id": responsible_id}

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.ASSIGN_RESPONSIBLE_TO_PVZ_GROUP,
        payload=payload_data,
        handler=lambda: service.assign_responsible(
            group_id=group_id,
            responsible_id=responsible_id,
            current_user_id=current_user.id,
        ),
    )


@pvz_groups_router.patch("/{group_id}", response_model=PVZGroupResponseSchema)
async def update_group(
    group_id: int,
    current_user: CurrentUserDep,
    data: PVZGroupUpdateSchema,
    event_id: IdempotencyKeyDep,
    service: PVZGroupsService = Depends(get_pvz_groups_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Обновляет существующую группу ПВЗ."""

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.UPDATE_PVZ_GROUP,
        payload=data.model_dump(mode="json"),
        handler=lambda: service.update_group(
            group_id=group_id,
            data=data,
            current_user_id=current_user.id,
        ),
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
    event_id: IdempotencyKeyDep,
    group_service: PVZGroupsService = Depends(get_pvz_groups_service),
    pvz_service: PVZService = Depends(get_pvz_service),
    inbox_service: InboxService = Depends(get_inbox_service),
):
    """Удаляет группу ПВЗ и отвязывает все её ПВЗ."""

    async def _handler():
        await pvz_service.unassign_all_pvz_from_group(group_id=group_id)
        await group_service.delete_group(
            group_id=group_id,
            current_user_id=current_user.id,
        )

    return await inbox_service.execute(
        event_id=event_id,
        event_type=EventType.DELETE_PVZ_GROUP,
        payload={"group_id": group_id},
        handler=_handler,
    )
