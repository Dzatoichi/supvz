from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.dao.baseDAO import BaseDAO, T
from src.models import Positions


class PositionDAO(BaseDAO[Positions]):
    """
    Класс DAO для работы с сущностями Positions.
    """

    def __init__(self):
        super().__init__(model=Positions)

    @BaseDAO.with_exception
    async def get_positions(self, owner_id: int):
        async with self._get_session() as session:
            stmt = select(self.model).filter_by(owner_id=owner_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    @BaseDAO.with_exception
    async def get_all(self):
        async with self._get_session() as session:
            stmt = select(self.model).options(selectinload(self.model.permissions))
            result = await session.execute(stmt)
            return result.scalars().all()

    @BaseDAO.with_exception
    async def get_position(self, *args, **kwargs) -> Positions | None:
        """
        Данный метод реализует поиск должности по любому аттрибуту,
        который будет указан в качестве аргумента функции.
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
    async def create(self, payload: dict, session: AsyncSession) -> Positions:
        """Метод создания пользователя"""
        user = Positions(**payload)
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

        updated = result.scalar_one_or_none()

        return updated
