from datetime import datetime, timedelta
from typing import Generic, TypeVar

from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.shifts import Shift
from src.schemas.shifts_schemas import ShiftCreateSchema, ShiftUpdateSchema

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
        Поддерживает передачу произвольных полей через kwargs.
        """
        data = cls.build(**kwargs)
        # Используем mode="python" чтобы сохранить datetime объекты
        data_dict = data.model_dump(mode="python")

        # Переопределяем поля из kwargs (для гибкости тестов)
        for key, value in kwargs.items():
            if key in data_dict:
                data_dict[key] = value

        # cls.__model_cls__ - ссылка на SQLAlchemy модель
        db_obj = cls.__model_cls__(**data_dict)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


class ShiftFactory(AsyncPersistenceFactory[ShiftCreateSchema]):
    """
    Фабрика для создания смен.

    Примеры использования:
        # Создание с дефолтными значениями
        shift = await ShiftFactory.create_async(session)

        # Создание с конкретным scheduled_shift_id
        shift = await ShiftFactory.create_async(session, scheduled_shift_id=42)

        # Создание активной смены (без ended_at)
        shift = await ShiftFactory.create_async(session, ended_at=None)

        # Создание завершенной смены
        shift = await ShiftFactory.create_async(
            session,
            started_at=datetime.now() - timedelta(hours=8),
            ended_at=datetime.now()
        )
    """

    __model__ = ShiftCreateSchema
    __model_cls__ = Shift

    scheduled_shift_id = Use(ModelFactory.__random__.randint, 1, 100)
    started_at = Use(lambda: datetime.now())
    ended_at = Use(lambda: None)


class ShiftUpdateFactory(ModelFactory[ShiftUpdateSchema]):
    """
    Фабрика для генерации данных обновления смены.

    Примеры использования:
        # Генерация данных для обновления
        update_data = ShiftUpdateFactory.build()

        # С конкретными значениями
        update_data = ShiftUpdateFactory.build(
            scheduled_shift_id=100,
            ended_at=datetime.now()
        )
    """

    __model__ = ShiftUpdateSchema

    scheduled_shift_id = Use(ModelFactory.__random__.randint, 1, 100)
    started_at = Use(lambda: datetime.now())
    ended_at = Use(lambda: None)


class ShiftDataGenerator:
    """
    Утилитный класс для генерации тестовых данных смен.
    Используется для параметризации тестов.
    """

    @staticmethod
    def valid_create_payloads():
        """Генерирует валидные payload для создания смен."""
        now = datetime.now()
        return [
            {"scheduled_shift_id": 1},
            {"scheduled_shift_id": 50, "started_at": now.isoformat()},
            {
                "scheduled_shift_id": 100,
                "started_at": now.isoformat(),
                "ended_at": (now + timedelta(hours=8)).isoformat(),
            },
        ]

    @staticmethod
    def invalid_create_payloads():
        """Генерирует невалидные payload для тестирования ошибок."""
        now = datetime.now()
        return [
            ({}, "missing_scheduled_shift_id"),
            ({"scheduled_shift_id": "abc"}, "invalid_type"),
            ({"scheduled_shift_id": None}, "null_value"),
            (
                {
                    "scheduled_shift_id": 1,
                    "started_at": now.isoformat(),
                    "ended_at": (now - timedelta(hours=1)).isoformat(),
                },
                "ended_before_started",
            ),
        ]

    @staticmethod
    def pagination_params():
        """Генерирует параметры для тестирования пагинации."""
        return [
            (1, 5, 5),
            (2, 5, 5),
            (1, 10, 10),
            (3, 5, 2),
        ]
