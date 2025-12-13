from polyfactory import Use

from src.models import Permissions
from src.schemas.permissions_schemas import PermissionReadSchema
from src.tests.factories.base_factories import AsyncPersistenceFactory, faker


class PermissionFactory(AsyncPersistenceFactory[Permissions]):
    """Фабрика для создания права доступа."""

    __model__ = PermissionReadSchema
    __model_cls__ = Permissions

    # Генерируем уникальное имя права, например "user:create", "order:view"
    code_name = Use(lambda: f"{faker.word()}:{faker.word()}_{faker.random_int()}")
    description = Use(faker.sentence)
