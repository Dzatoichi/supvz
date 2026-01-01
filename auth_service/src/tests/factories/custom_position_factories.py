from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CustomPositions
from src.schemas.custom_positions_schemas import CustomPositionCreateSchema, CustomPositionUpdateSchema
from src.tests.factories.base_factories import AsyncPersistenceFactory, faker


class CustomPositionFactory(AsyncPersistenceFactory[CustomPositionCreateSchema]):
    """
    Фабрика для создания кастомной должности В БД.
    """

    __model__ = CustomPositionCreateSchema
    __model_cls__ = CustomPositions

    title = Use(faker.job)
    owner_id = Use(faker.pyint, min_value=1, max_value=1000)
    permission_ids = Use(lambda: [])  # Генерируем пустой список (или можно любой)

    @classmethod
    async def create_async(cls, session: AsyncSession, **kwargs):
        """
        Переопределяем метод, чтобы исключить permission_ids
        из конструктора SQLAlchemy модели.
        """
        # 1. Генерируем Pydantic схему
        schema_instance = cls.build(**kwargs)

        # 2. Преобразуем в dict и УДАЛЯЕМ поле, которого нет в модели БД
        data = schema_instance.model_dump()
        data.pop("permission_ids", None)

        # 3. Создаём SQLAlchemy объект только с валидными полями
        db_obj = cls.__model_cls__(**data)
        session.add(db_obj)
        await session.flush()

        return db_obj


class CustomPositionCreatePayloadFactory(ModelFactory[CustomPositionCreateSchema]):
    """Фабрика для POST запроса (JSON body)"""

    __model__ = CustomPositionCreateSchema

    title = Use(faker.job)
    owner_id = Use(faker.pyint, min_value=1, max_value=1000)
    permission_ids = Use(lambda: [1])  # Заглушка, переопределяем в тестах


class CustomPositionUpdatePayloadFactory(ModelFactory[CustomPositionUpdateSchema]):
    """Фабрика для PATCH запроса (JSON body)"""

    __model__ = CustomPositionUpdateSchema

    title = Use(faker.job)
    permission_ids = Use(lambda: [1])  # Заглушка, переопределяем в тестах
