from typing import Generic, TypeVar

from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.employees.employees import Employees
from src.models.pvzs.PVZGroups import PVZGroups
from src.models.pvzs.PVZs import PVZs
from src.schemas.employees_schemas import EmployeeCreateRequestSchema
from src.schemas.pvz_group_schemas import PVZGroupCreateSchema
from src.schemas.pvz_schemas import PVZAdd, PVZUpdate

T = TypeVar("T", bound=BaseModel)


class AsyncPersistenceFactory(ModelFactory[T], Generic[T]):
    """
    Базовый класс фабрики, который добавляет метод .create_async(session)
    """

    __is_base_factory__ = True

    @classmethod
    async def create_async(cls, session: AsyncSession, **kwargs):
        """
        Генерирует данные, создает модель SQLAlchemy и сохраняет в БД.
        """
        data = cls.build(**kwargs)
        data_dict = data.model_dump(mode="json")

        # cls.__model_cls__ - это ссылка на SQLAlchemy модель
        db_obj = cls.__model_cls__(**data_dict)

        session.add(db_obj)
        await session.flush()
        return db_obj


class GroupFactory(AsyncPersistenceFactory[PVZGroupCreateSchema]):
    __model__ = PVZGroupCreateSchema
    __model_cls__ = PVZGroups


class EmployeeFactory(AsyncPersistenceFactory[EmployeeCreateRequestSchema]):
    __model__ = EmployeeCreateRequestSchema
    __model_cls__ = Employees

    phone_number = Use(lambda: ModelFactory.__faker__.numerify(text="+7##########"))


class PVZFactory(AsyncPersistenceFactory[PVZAdd]):
    __model__ = PVZAdd
    __model_cls__ = PVZs

    group_id = None


class PVZUpdateFactory(AsyncPersistenceFactory[PVZUpdate]):
    __model__ = PVZUpdate
