from polyfactory import Use
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import SystemPositions
from src.models.position_permissions.system_position_permissions import SystemPositionPermissions
from src.schemas.system_positions_schemas import SystemPositionBaseSchema
from src.tests.factories.base_factories import AsyncPersistenceFactory
from src.tests.factories.permission_factories import PermissionFactory


class SystemPositionFactory(AsyncPersistenceFactory[SystemPositionBaseSchema]):
    """
    Фабрика системных должностей.

    - build() -> SystemPositionSchema
    - create_async() -> SystemPositions (в БД)
    """

    __model__ = SystemPositionBaseSchema
    __model_cls__ = SystemPositions

    title = Use(lambda: f"Position_{id(object())}")

    @classmethod
    async def create_with_permissions(cls, session: AsyncSession, **kwargs):
        position = await cls.create_async(session, **kwargs)

        permission = await PermissionFactory.create_async(session)

        stmt = insert(SystemPositionPermissions).values(system_position_id=position.id, permission_id=permission.id)
        await session.execute(stmt)
        await session.flush()

        return position
