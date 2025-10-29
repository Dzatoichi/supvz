from fastapi import HTTPException, status

from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate


class PVZService:
    async def add_pvz(
        self,
        data: PVZAdd,
        repo: PVZsDAO,
        group_repo: PVZGroupsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(code=data.code)
        if pvz:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"PVZ с кодом {data.code} уже существует",
            )

        # Если указан group_id, проверяем владельца
        if data.group_id:
            group = await group_repo.get_group(id=data.group_id)
            if not group:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail=f"Группа {data.group_id} не найдена",
                )

            # Проверяем, что owner_id ПВЗ совпадает с owner_id группы
            if data.owner_id != group.owner_id:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Невозможно добавить ПВЗ: owner_id={data.owner_id} "
                        f"не совпадает с owner_id группы={group.owner_id}"
                    ),
                )

        pvz_add = await repo.create(data.model_dump())
        return PVZRead.model_validate(pvz_add, from_attributes=True)

    async def update_pvz_by_id(
        self,
        pvz_id: int,
        data: PVZUpdate,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pvz not found")
        payload = {
            "address": data.address,
            "owner_id": data.owner_id,
            "curator_id": data.curator_id,
            "group": data.group,
        }
        pvz_update = await repo.update(id=pvz_id, **payload)

        return PVZRead.model_validate(pvz_update)

    async def get_pvz_by_id(
        self,
        pvz_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pvz not found")

        return PVZRead.model_validate(pvz)

    async def get_pvzs(
        self,
        code: str,
        type: str,
        address: str,
        group_id: int,
        repo: PVZsDAO,
    ) -> list[PVZRead]:
        filters = {}
        if code is not None:
            filters["code"] = code
        if type is not None:
            filters["type"] = type
        if address is not None:
            filters["address"] = address
        if group_id is not None:
            filters["group_id"] = group_id
        pvzs = await repo.get_pvzs(**filters)

        return [PVZRead.model_validate(pvz) for pvz in pvzs]

    async def delete_pvz_by_id(
        self,
        pvz_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pvz not found")
        pvz_info = {
            "id": pvz.id,
            "code": pvz.code,
            "type": pvz.type,
            "address": pvz.address,
            "owner_id": pvz.owner_id,
            "group": pvz.group,
            "curator_id": pvz.curator_id,
            "created_at": pvz.created_at,
        }
        success = await repo.delete(id=pvz_id)
        if not success:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete PVZ")

        return pvz_info
