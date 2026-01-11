from functools import wraps
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import Base

T = TypeVar("T", bound=Base)
S = TypeVar("S", bound=BaseModel)


class BaseDAO(Generic[T]):
    """Базовый DAO для работы с БД."""

    model: type[T]

    def __init__(self, session: AsyncSession, model: type[T] | None = None):
        """Инициализация DAO."""
        self.session = session
        if model is not None:
            self.model = model

        if not hasattr(self, "model") or self.model is None:
            raise TypeError("Отсутствует модель")

    @staticmethod
    def with_exception(func):
        """Декоратор для обработки ошибок SQLAlchemy."""

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except SQLAlchemyError as e:
                raise e
            except Exception as e:
                raise e

        return async_wrapper

    @with_exception
    async def create(self, data: S) -> T:
        """Создание записи в БД."""
        obj = self.model(**data.model_dump(exclude_unset=True))
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    @with_exception
    async def get_by_id(self, id: int) -> T | None:
        """Получение записи по ID."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @with_exception
    async def get_all(self) -> list[T]:
        """Получение всех записей."""
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    @with_exception
    async def update(self, id: int, data: S) -> T | None:
        """Обновление записи."""
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return await self.get_by_id(id)
        stmt = update(self.model).where(self.model.id == id).values(**update_data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        updated = result.scalar_one_or_none()
        if updated:
            await self.session.refresh(updated)
        return updated

    @with_exception
    async def delete(self, id: int) -> bool:
        """Удаление записи."""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
