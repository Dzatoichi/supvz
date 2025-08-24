from typing import Generic, TypeVar, Optional, List, Type, Any, Dict
from contextlib import asynccontextmanager

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import Select

from auth_service.src.database.base import Base, db_helper

T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    def __init__(self, model: Optional[Type[T]] = None):
        if model is not None:
            self.model = model

        if self.model is None:
            raise TypeError("Отсутствует модель")

        self._db_helper = db_helper

    @asynccontextmanager
    async def _get_session(self) -> AsyncSession:
        async with self._db_helper.async_session_maker() as session:
            try:
                yield session
            except SQLAlchemyError:
                await session.rollback()
                raise

    async def create(self, payload: Dict[str, Any]) -> T:
        obj = self.model(**payload)
        async with self._get_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def get_by_id(self, id: int) -> Optional[T]:
        stmt: Select = select(self.model).where(self.model.id == id)
        async with self._get_session() as session:
            res = await session.execute(stmt)
            return res.scalars().first()

    async def get_all(self) -> List[T]:
        stmt = select(self.model)
        async with self._get_session() as session:
            res = await session.execute(stmt)
            return res.scalars().all()

    async def update(self, id: int, **kwargs) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        async with self._get_session() as session:
            res = await session.execute(stmt)
            await session.commit()
            updated = res.scalars().first()
            if updated is not None:
                await session.refresh(updated)

    async def delete(self, id: int) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        async with self._get_session() as session:
            await session.execute(stmt)
            await session.commit()