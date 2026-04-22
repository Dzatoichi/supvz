from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.pvzs.PVZGroups import PVZGroups


class PVZGroupsDAO(BaseDAO[PVZGroups]):
    """
    Класс, наследующий базовый DAO для работы с сущностями ПВЗ групп.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(model=PVZGroups, session=session)

    @BaseDAO.with_exception
    async def get_group(self, *args, **kwargs) -> Optional[PVZGroups]:
        """
        Получает одну группу ПВЗ по любым указанным атрибутам.
        Возвращает объект PVZGroups или None, если группа не найдена.
        """
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @BaseDAO.with_exception
    async def get_groups(self, *args, **kwargs) -> Optional[list[PVZGroups]]:
        """
        Получает список групп ПВЗ по любым указанным атрибутам.
        Возвращает список объектов PVZGroups. Если группы не найдены, возвращает пустой список.
        """
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    @BaseDAO.with_exception
    async def set_responsible(self, group_id: int, responsible_id: int):
        stmt = update(self.model).where(self.model.id == group_id).values(responsible_id=responsible_id)
        await self.session.execute(stmt)
