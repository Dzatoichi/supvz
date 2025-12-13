from polyfactory import Use
from pydantic import BaseModel

from src.models import SystemPositions
from src.models.position_permissions.system_position_permissions import SystemPositionPermissions
from src.schemas.system_positions_schemas import SystemPositionBaseSchema
from src.tests.factories.base_factories import AsyncPersistenceFactory, faker


class SystemPositionPermissionLinkSchema(BaseModel):
    title: str
    system_position_id: int
    permission_id: int


class SystemPositionFactory(AsyncPersistenceFactory[SystemPositionBaseSchema]):
    """
    Фабрика для создания системной должности в БД.
    """

    __model__ = SystemPositionPermissionLinkSchema
    __model_cls__ = SystemPositions

    title = Use(faker.job)

    @classmethod
    def _build_db_object(cls, data: SystemPositionPermissionLinkSchema):
        return SystemPositions(**data.model_dump())


class SystemPositionPermissionLinkFactory(AsyncPersistenceFactory[SystemPositionPermissions]):
    """
    Фабрика для СВЯЗИ.
    """

    __model__ = SystemPositionPermissionLinkSchema
    __model_cls__ = SystemPositionPermissions

    system_position_id = Use(faker.pyint)
    permission_id = Use(faker.pyint)
