from typing import Optional

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO, T
from src.models import Positions


class PositionDAO(BaseDAO[Positions]):
    """
    Класс DAO для работы с сущностями Positions.
    """

    def __init__(self):
        super().__init__(model=Positions)

    @BaseDAO.with_exception
    async def get_positions(
        self,
        params: Params,
        owner_id: int | None = None,
    ) -> Page[Positions]:
        """
        Получает список должностей с фильтрацией и пагинацией.
        """
        async with self._get_session() as session:
            stmt = select(self.model)

            if owner_id is not None:
                stmt = stmt.where(self.model.owner_id == owner_id)

            stmt = stmt.order_by(self.model.id.desc())

            return await paginate(session, stmt, params)

    @BaseDAO.with_exception
    async def get_position(self, *args, session: AsyncSession, **kwargs) -> Positions | None:
        """
        Данный метод реализует поиск должности по любому аттрибуту,
        который будет указан в качестве аргумента функции.
        """
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @BaseDAO.with_exception
    async def create(self, payload: dict, session: AsyncSession) -> Positions:
        """Метод создания пользователя"""
        user = self.model(**payload)
        session.add(user)
        await session.flush()
        return user

    @BaseDAO.with_exception
    async def update(
        self,
        position_id: int,
        session: AsyncSession,
        **kwargs,
    ) -> Optional[T]:
        """Метод обновления должности"""

        stmt = update(self.model).where(self.model.id == position_id).values(**kwargs).returning(self.model)

        result = await session.execute(stmt)

        return result.scalar_one_or_none()
