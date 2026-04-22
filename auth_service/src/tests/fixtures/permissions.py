import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.enums import PositionSourceEnum
from src.tests.factories.permission_factories import PermissionFactory
from src.tests.factories.system_position_factories import SystemPositionFactory
from src.tests.factories.user_factories import UserFactory, UserPermissionFactory


@pytest.fixture
async def permissions_test_data(session: AsyncSession) -> dict:
    """
    Фикстура создаёт полный набор данных для тестов permissions.
    Возвращает словарь с ID созданных объектов.
    """
    position_1 = await SystemPositionFactory.create_with_permissions(session)
    position_2 = await SystemPositionFactory.create_with_permissions(session)

    user = await UserFactory.create_async(
        session,
        position_id=position_1.id,
        position_source=PositionSourceEnum.system,
    )

    direct_permission = await PermissionFactory.create_async(session)

    await UserPermissionFactory.create_async(
        session,
        user_id=user.id,
        permission_id=direct_permission.id,
    )

    return {
        "position_1_id": position_1.id,
        "position_2_id": position_2.id,
        "user_id": user.id,
    }
