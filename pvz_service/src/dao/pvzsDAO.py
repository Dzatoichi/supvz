from typing import Optional

from sqlalchemy import select
from src.dao.baseDAO import BaseDAO

from src.models.pvzs.PVZs import PVZs


class PVZsDAO(BaseDAO[PVZs]):
    def __init__(self):
        super().__init__(model=PVZs)

    @BaseDAO.with_exceptions
    async def get_pvz(self, *args, **kwargs) -> Optional[PVZs]:
        """
        Данный метод реализует поиск по любому аттрибуту, который будет указан в качестве аргумента функции.
        Если будет необходимо, можно будет переписать все методы таким образом, если нет - уберу.
        """
        async with self._get_session() as session:
            stmt = select(self.model)
            if args:
                stmt = stmt.filter(*args)
            if kwargs:
                stmt = stmt.filter_by(**kwargs)

            result = await session.execute(stmt)
            return result.scalar_one_or_none()