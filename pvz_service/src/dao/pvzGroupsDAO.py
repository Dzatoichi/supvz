from typing import Optional

from sqlalchemy import select, update

from src.dao.baseDAO import BaseDAO
from src.models.pvzs.PVZGroups import PVZGroups
from src.models.pvzs.PVZs import PVZs


class PVZGroupsDAO(BaseDAO[PVZGroups]):
    def __init__(self):
        super().__init__(model=PVZGroups)

    @BaseDAO.with_exception
    async def update_pvzs_curator_by_group(self, group_id: int, curator_id: int):
        """
        Обновляет поле curator_id у всех ПВЗ, принадлежащих указанной группе.
        """
        async with self._get_session() as session:
            stmt = update(PVZs).where(PVZs.group_id == group_id).values(curator_id=curator_id)
            await session.execute(stmt)
            await session.commit()

    @BaseDAO.with_exception
    async def get_group(self, *args, **kwargs) -> Optional[PVZGroups]:
        """
        Получает одну группу ПВЗ по любым указанным атрибутам.
        Возвращает объект PVZGroups или None, если группа не найдена.
        """
        async with self._get_session() as session:
            stmt = select(self.model)
            if args:
                stmt = stmt.filter(*args)
            if kwargs:
                stmt = stmt.filter_by(**kwargs)

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @BaseDAO.with_exception
    async def get_groups(self, *args, **kwargs) -> Optional[list[PVZGroups]]:
        """
        Получает список групп ПВЗ по любым указанным атрибутам.
        Возвращает список объектов PVZGroups. Если группы не найдены, возвращает пустой список.
        """
        async with self._get_session() as session:
            stmt = select(self.model)
            if args:
                stmt = stmt.filter(*args)
            if kwargs:
                stmt = stmt.filter_by(**kwargs)

            result = await session.execute(stmt)
            return result.scalars().all()
