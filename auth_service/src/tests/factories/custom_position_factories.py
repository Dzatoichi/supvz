import random

from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.models import CustomPositions
from src.schemas.custom_positions_schemas import CustomPositionCreateSchema, CustomPositionUpdateSchema
from src.tests.factories.base_factories import AsyncPersistenceFactory, faker


class CustomPositionFactory(AsyncPersistenceFactory[CustomPositionCreateSchema]):
    """
    Фабрика для создания кастомной должности в БД.
    """

    __model__ = CustomPositionCreateSchema
    __model_cls__ = CustomPositions

    title = Use(faker.job)
    owner_id = Use(faker.pyint, min_value=1, max_value=1000)

    permission_ids = Use(lambda: [faker.pyint(min_value=1, max_value=50) for _ in range(random.randint(0, 3))])


class CustomPositionCreatePayloadFactory(ModelFactory[CustomPositionCreateSchema]):
    """Фабрика для POST запроса создания должности"""

    __model__ = CustomPositionCreateSchema

    title = Use(faker.job)
    owner_id = Use(faker.pyint, min_value=1, max_value=1000)

    permission_ids = Use(lambda: [faker.pyint(min_value=1, max_value=50) for _ in range(random.randint(1, 3))])


class CustomPositionUpdatePayloadFactory(ModelFactory[CustomPositionUpdateSchema]):
    """Фабрика для PATCH запроса обновления должности"""

    __model__ = CustomPositionUpdateSchema

    title = Use(faker.job)

    permission_ids = Use(lambda: [faker.pyint(min_value=1, max_value=50) for _ in range(random.randint(1, 3))])
