from typing import Generic, TypeVar

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=BaseModel)


class AsyncPersistenceFactory(ModelFactory[T], Generic[T]):
    """
    Базовый класс фабрики, который добавляет метод .create_async(session)
    """

    __is_base_factory__ = True

    @classmethod
    async def create_async(cls, session: AsyncSession, **kwargs):
        data = cls.build(**kwargs)

        if not cls.__model_cls__:
            raise ValueError("__model_cls__ is not defined")

        db_obj = cls._build_db_object(data)
        session.add(db_obj)
        await session.flush()
        return db_obj

    @classmethod
    def _build_db_object(cls, data: T):
        raise NotImplementedError
