from fastapi import HTTPException, status

from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.models.pvzs.PVZs import PVZs
from src.schemas.pvz_group_schemas import (
    PVZGroupCreateSchema,
    PVZGroupResponseSchema,
    PVZGroupUpdateSchema,
)
from src.schemas.pvz_schemas import PVZRead


class PVZGroupsService:
    async def create_group(
        self,
        data: PVZGroupCreateSchema,
        repo: PVZGroupsDAO,
    ):
        """Создаёт новую группу ПВЗ"""
        payload = data.model_dump()
        group = await repo.create(payload)

        return PVZGroupResponseSchema.model_validate(group)

    async def update_group(
        self,
        group_id: int,
        data: PVZGroupUpdateSchema,
        repo: PVZGroupsDAO,
    ):
        """Обновляет данные группы ПВЗ и кураторство для ПВЗ при необходимости."""

        group = await repo.update(group_id, **data.model_dump(exclude_unset=True))

        if data.curator_id:
            await repo.update_pvzs_curator_by_group(group_id, data.curator_id)

        return PVZGroupResponseSchema.model_validate(group)

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

    async def get_groups(
        self,
        params: dict,
        repo: PVZGroupsDAO,
    ) -> list[PVZGroupResponseSchema] | PVZGroupResponseSchema:
        """Возвращает группы по owner_id или curator_id."""

        actual_params = {key: value for key, value in params.items() if value is not None}

        # Если не передали ни одного параметра — вернуть все группы
        if len(actual_params) == 0:
            groups = await repo.get_all()
            return [PVZGroupResponseSchema.model_validate(g) for g in groups]

        if len(actual_params) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Используйте только один параметр для поиска.",
            )

        field_name, field_value = next(iter(actual_params.items()))

        groups = await repo.get_groups(**{field_name: field_value})

        if not groups:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Группы не найдены",
            )

        return [PVZGroupResponseSchema.model_validate(g) for g in groups]

    async def get_group_with_pvzs(
        self,
        group_id,
        repo: PVZGroupsDAO,
    ):
        """Возвращает одну группу ПВЗ по ID с информацией о ПВЗ."""

        group = await repo.get_by_id(group_id)

        if not group:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Группа не найдена")

        return PVZGroupResponseSchema.model_validate(group)

    async def delete_group(
        self,
        group_id,
        repo: PVZGroupsDAO,
        pvz_repo: PVZsDAO,
    ):
        """Удаляет группу ПВЗ и отвязывает все её ПВЗ."""

        await pvz_repo.unassign_pvzs_from_group(group_id)

        await repo.delete(id=group_id)

    async def assign_pvz_to_group(
        self,
        group_id: int,
        pvz_ids: list[int],
        repo: PVZGroupsDAO,
        pvz_repo: PVZsDAO,
    ):
        group = await repo.get_group(id=group_id)
        if not group:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Группа не найдена")

        # Получаем все ПВЗ, которые хотим привязать
        pvzs = await pvz_repo.get_pvzs(PVZs.id.in_(pvz_ids))

        if len(pvzs) != len(pvz_ids):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Некоторые ПВЗ не существуют")

        # Проверяем, что у всех ПВЗ owner_id совпадает с owner_id группы
        for pvz in pvzs:
            if pvz.owner_id != group.owner_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ПВЗ {pvz.id} принадлежит другому владельцу",
                )

        await repo.assign_pvz_to_group(group_id=group_id, pvz_ids=pvz_ids)

        return {"detail": "ПВЗ успешно привязаны к группе"}

    async def assign_curator(self, group_id: int, curator_id: int, repo: PVZGroupsDAO):
        """Привязывает куратора к группе, а также ко всем пвз состоящим в этой группе"""

        await repo.set_curator_for_group(group_id, curator_id)
        return {"detail": "Куратор успешно назначен и применён ко всем ПВЗ группы"}
