from fastapi import HTTPException, status

from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_group_schemas import (
    PVZGroupCreate,
    PVZGroupResponse,
    PVZGroupUpdate,
)
from src.schemas.pvz_schemas import PVZRead


class PVZGroupsService:
    async def create_group(
        self,
        data: PVZGroupCreate,
        repo: PVZGroupsDAO,
    ):
        """Создаёт новую группу ПВЗ и назначает куратора всем ПВЗ группы."""
        payload = data.model_dump()
        group = await repo.create(payload)

        # если указан куратор — обновим все ПВЗ этой группы
        if data.curator_id:
            await repo.update_pvzs_curator_by_group(group.id, data.curator_id)

        return PVZGroupResponse.model_validate(group)

    async def update_group(
        self,
        group_id: int,
        data: PVZGroupUpdate,
        repo: PVZGroupsDAO,
    ):
        """Обновляет данные группы ПВЗ и кураторство для ПВЗ при необходимости."""

        group = await repo.update(group_id, **data.model_dump(exclude_unset=True))

        if data.curator_id:
            await repo.update_pvzs_curator_by_group(group_id, data.curator_id)

        return PVZGroupResponse.model_validate(group)

    async def get_pvzs_by_group(
        self,
        group_id: int | None,
        group_name: str | None,
        pvz_repo: PVZsDAO,
        group_repo: PVZGroupsDAO,
    ):
        """Возвращает список ПВЗ по ID или имени группы."""

        if (group_id is None and group_name is None) or (group_id is not None and group_name is not None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нужно передать ровно один параметр — group_id или group_name",
            )

        if group_name:
            group = await group_repo.get_group(name=group_name)
            if not group:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
            group_id = group.id

        pvzs = await pvz_repo.get_pvzs(group_id=group_id)
        return [PVZRead.model_validate(p) for p in pvzs]

    async def get_groups_by_id(
        self,
        params: dict,
        repo: PVZGroupsDAO,
    ) -> list[PVZGroupResponse] | PVZGroupResponse:
        """Возвращает группы по owner_id или curator_id."""

        actual_params = {k: v for k, v in params.items() if v is not None}

        if len(actual_params) == 0:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Нужно указать хотя бы один параметр (owner_id или curator_id).",
            )

        if len(actual_params) > 1:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Используйте только один параметр для поиска.",
            )

        field_name, field_value = next(iter(actual_params.items()))

        groups = await repo.get_groups(**{field_name: field_value})

        if not groups:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Группы не найдены",
            )

        return [PVZGroupResponse.model_validate(g) for g in groups]

    async def get_group_with_pvzs(
        self,
        group_id,
        repo: PVZGroupsDAO,
    ):
        """Возвращает одну группу ПВЗ по ID с информацией о ПВЗ."""

        group = await repo.get_by_id(group_id)

        if not group:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Группа не найдена")

        return PVZGroupResponse.model_validate(group)

    async def get_groups(
        self,
        repo: PVZGroupsDAO,
    ):
        """Возвращает список всех групп ПВЗ."""

        groups = await repo.get_all()

        if not groups:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Группы не найдены")

        return [PVZGroupResponse.model_validate(g) for g in groups]

    async def delete_group(
        self,
        group_id,
        repo: PVZGroupsDAO,
        pvz_repo: PVZsDAO,
    ):
        """Удаляет группу ПВЗ и отвязывает все её ПВЗ."""

        await pvz_repo.unassign_pvzs_from_group(group_id)

        await repo.delete(id=group_id)
