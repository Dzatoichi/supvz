from functools import wraps
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    """
    Базовый класс DAO для работы с ORM-моделями.
    """

    def __init__(self, session: AsyncSession, model: Optional[Type[T]] = None):
        """
        Метод инициализации.
        """
        self.session = session
        if model is not None:
            self.model = model

        if not hasattr(self, "model") or self.model is None:
            raise TypeError("Отсутствует модель")

    @staticmethod
    def with_exception(func):
        """
        Декоратор, оборачивающий метод для обработки и проброса исключения дальше.
        """

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
    async def create(self, payload: Dict[str, Any]) -> T:
        """
        Базовый метод создания сущности.
        """
        obj = self.model(**payload)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    @with_exception
    async def get_by_id(self, id: int) -> Optional[T]:
        """
        Базовый метод получения сущности по id.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @with_exception
    async def get_all(self) -> List[T]:
        """
        Базовый метод получения сущностей.
        """
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    @with_exception
    async def update(self, id: int, **kwargs) -> Optional[T]:
        """
        Базовый метод изменения сущностей.
        """
        stmt = update(self.model).where(self.model.id == id).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        updated = result.scalar_one_or_none()
        if updated:
            await self.session.refresh(updated)
        return updated

    @with_exception
    async def delete(self, **filters) -> bool:
        stmt = delete(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0
