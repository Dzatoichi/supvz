import uuid

from polyfactory import Use

from src.models import Permissions
from src.schemas.permissions_schemas import PermissionBaseSchema
from src.tests.factories.base_factories import AsyncPersistenceFactory


class PermissionFactory(AsyncPersistenceFactory[PermissionBaseSchema]):
    """
    Фабрика прав доступа.
    """

    __model__ = PermissionBaseSchema
    __model_cls__ = Permissions

    code_name = Use(lambda: f"permission:{uuid.uuid4().hex}")
    description = "Test permission"
