"""
Базовые классы фабрик.
"""

from typing import Generic, TypeVar

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=BaseModel)


class AsyncPersistenceFactory(ModelFactory[T], Generic[T]):
    """
    Базовый класс фабрики:
    - build() -> Pydantic схема (для payload)
    - create_async() -> SQLAlchemy модель (в БД)
    """

    __is_base_factory__ = True
    __model_cls__ = None

    @classmethod
    async def create_async(cls, session: AsyncSession, **kwargs):
        """
        Генерирует данные, создает модель SQLAlchemy и сохраняет в БД.
        """
        data = cls.build(**kwargs)
        data_dict = data.model_dump(mode="json")

        if cls.__model_cls__ is None:
            raise ValueError(f"__model_cls__ is not defined for {cls.__name__}")

        db_obj = cls.__model_cls__(**data_dict)

        session.add(db_obj)
        await session.flush()
        return db_obj

    @classmethod
    async def create_batch_async(
        cls,
        session: AsyncSession,
        size: int,
        **kwargs,
    ):
        """
        Создаёт несколько объектов в БД.
        """
        return [await cls.create_async(session, **kwargs) for _ in range(size)]
