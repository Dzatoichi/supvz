from sqlalchemy import select

from src.dao.baseDAO import BaseDAO
from src.models import Positions


class PositionDAO(BaseDAO[Positions]):
    """
    Класс DAO для работы с сущностями Positions.
    """

    def __init__(self):
        super().__init__(model=Positions)

    @BaseDAO.with_exception
    async def get_positions(self, *args, **kwargs) -> list[Positions] | None:
        """
        Данный метод реализует поиск по любому аттрибуту,
        который будет указан в качестве аргумента функции.
        """
        async with self._get_session() as session:
            stmt = select(self.model)
            if args:
                stmt = stmt.filter(*args)
            if kwargs:
                stmt = stmt.filter_by(**kwargs)

            result = await session.execute(stmt)
            return result.scalars().all()
