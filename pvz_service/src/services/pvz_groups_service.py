from fastapi import HTTPException, status

from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_group_schemas import (
    PVZGroupCreateSchema,
    PVZGroupResponseSchema,
    PVZGroupUpdateSchema,
)


class PVZGroupsService:
    def __init__(self, db_helper):
        self.db_helper = db_helper

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
        repo: PVZsDAO,
    ):
        """Обновляет данные группы ПВЗ и кураторство для ПВЗ при необходимости."""

        group = await repo.update(group_id, **data.model_dump(exclude_unset=True))

        if data.curator_id:
            await repo.update_pvzs_curator_by_group(group_id, data.curator_id)

        return PVZGroupResponseSchema.model_validate(group)

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
    ):
        """Удаляет группу ПВЗ."""

        await repo.delete(id=group_id)

    async def assign_curator(self, group_id: int, curator_id: int, repo: PVZGroupsDAO, pvz_repo: PVZsDAO):
        """Привязывает куратора к группе, а также ко всем пвз состоящим в этой группе"""

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():  # ← одна транзакция
                await repo.set_curator(group_id, curator_id, session)
                await pvz_repo.set_curator_for_group(group_id, curator_id, session)

        return {"detail": "Куратор успешно назначен и применён ко всем ПВЗ группы"}
