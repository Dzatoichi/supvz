import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.factories.custom_position_factories import CustomPositionFactory
from src.tests.factories.system_position_factories import SystemPositionFactory
from src.tests.factories.user_factories import UserFactory


@pytest.fixture
async def positions_test_data(session: AsyncSession) -> dict:
    """Фикстура создаёт тестовые данные."""
    system_pos = await SystemPositionFactory.create_with_permissions(session)

    user = await UserFactory.create_async(session)

    custom_pos = await CustomPositionFactory.create_async(session, owner_id=user.id)

    return {
        "system_pos_id": system_pos.id,
        "custom_pos_id": custom_pos.id,
        "user_id": user.id,
    }
