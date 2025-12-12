from typing import Optional

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO, T
from src.models import CustomPositions, SystemPositions


class CustomPositionDAO(BaseDAO[CustomPositions]):
    """
    Класс DAO для работы с сущностями CustomPositions.
    """

    def __init__(self):
        super().__init__(model=CustomPositions)

    @BaseDAO.with_exception
    async def get_positions(
        self,
        params: Params,
        owner_id: int | None = None,
    ) -> Page[CustomPositions]:
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
    async def get_position(self, *args, session: AsyncSession, **kwargs) -> CustomPositions | None:
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
    async def create(self, payload: dict, session: AsyncSession) -> CustomPositions:
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


class SystemPositionDAO(BaseDAO[SystemPositions]):
    """
    Класс DAO для работы с сущностями SystemPositions.
    """

    def __init__(self):
        super().__init__(model=SystemPositions)

    @BaseDAO.with_exception
    async def get_positions(
        self,
        params: Params,
    ) -> Page[SystemPositions]:
        """
        Получает список должностей с фильтрацией и пагинацией.
        """
        async with self._get_session() as session:
            stmt = select(self.model).order_by(self.model.id.desc())

            return await paginate(session, stmt, params)
