import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.enums import PositionSourceEnum
from src.tests.factories.system_position_factories import SystemPositionFactory

PERMISSIONS_URL = "/permissions/"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "param_keys, expected_min_total",
    [
        ({}, 1),
        ({"user_id": "user_id"}, 1),
        ({"position_source": PositionSourceEnum.system}, 1),
        ({"position_id": "position_1_id", "position_source": PositionSourceEnum.system}, 1),
    ],
    ids=[
        "no_filters",
        "filter_by_user",
        "filter_by_source",
        "filter_by_position_and_source",
    ],
)
async def test_get_permissions_with_filters(
    client: AsyncClient,
    session: AsyncSession,
    permissions_test_data: dict,
    param_keys: dict,
    expected_min_total: int,
):
    """
    Тест: Получение прав с различными комбинациями фильтров.
    GET /permissions/

    Сценарий:
    1. Фикстура создаёт должности и пользователя с правами.
    2. Отправляем запрос с указанными фильтрами.
    3. Проверяем, что возвращается корректный пагинированный ответ.
    """
    params = {}
    for key, value in param_keys.items():
        if hasattr(value, "value"):
            params[key] = value.value
        elif isinstance(value, str) and value in permissions_test_data:
            params[key] = permissions_test_data[value]
        else:
            params[key] = value

    response = await client.get(PERMISSIONS_URL, params=params)

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= expected_min_total


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "page, size",
    [
        (1, 1),
        (1, 10),
        (2, 1),
    ],
    ids=[
        "first_page_size_1",
        "first_page_size_10",
        "second_page_size_1",
    ],
)
async def test_get_permissions_pagination(
    client: AsyncClient,
    session: AsyncSession,
    page: int,
    size: int,
):
    """
    Тест: Проверка пагинации.
    GET /permissions/?page={page}&size={size}

    Сценарий:
    1. В БД создаются права.
    2. Запрашиваем с разными параметрами пагинации.
    3. Проверяем корректность page/size в ответе.
    """
    await SystemPositionFactory.create_with_permissions(session)

    response = await client.get(PERMISSIONS_URL, params={"page": page, "size": size})

    assert response.status_code == 200
    resp_data = response.json()
    assert len(resp_data["items"]) <= size
    assert resp_data["page"] == page
    assert resp_data["size"] == size
