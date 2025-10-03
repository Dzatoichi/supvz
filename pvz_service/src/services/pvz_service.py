from fastapi import HTTPException, status

from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_schemas import PVZBase, PVZGroup


class PVZService:
    async def add_group(
        self,
        data: PVZGroup,
        repo: PVZsDAO
    ) -> PVZBase:
        pvz = await repo.get_pvz(data.id)
        if not pvz:
            raise HTTPException(status.HTTP_409_CONFLICT, "Пункт не найден")

        await repo.add_group(id=data.id, group=data.group)

        return PVZBase(
            code=pvz.code,
            type=pvz.type,
            group=pvz.group,
        )
