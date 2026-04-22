import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CustomPositions
from src.schemas.enums import PositionSourceEnum
from src.tests.factories.custom_position_factories import (
    CustomPositionCreatePayloadFactory,
    CustomPositionFactory,
    CustomPositionUpdatePayloadFactory,
)
from src.tests.factories.permission_factories import PermissionFactory
from src.tests.factories.user_factories import UserFactory

POSITIONS_URL = "/positions"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "param_keys, expected_min_total",
    [
        ({"position_source": PositionSourceEnum.system}, 1),
        ({"owner_id": "user_id", "position_source": PositionSourceEnum.custom}, 1),
    ],
    ids=["get_system_positions", "get_custom_positions_by_owner"],
)
async def test_get_positions_list(
    client: AsyncClient,
    positions_test_data: dict,
    param_keys: dict,
    expected_min_total: int,
):
    """
    Тест: Получение списка должностей с фильтрацией.
    GET /positions/

    Сценарий:
    1. Фикстура создаёт системные и кастомные должности в БД.
    2. Отправляем запрос с фильтрами (по источнику или владельцу).
    3. Проверяем, что возвращается корректный пагинированный список (total >= expected).
    """
    params = {}
    for key, value in param_keys.items():
        if hasattr(value, "value"):
            params[key] = value.value
        elif isinstance(value, str) and value in positions_test_data:
            params[key] = positions_test_data[value]
        else:
            params[key] = value

    response = await client.get(POSITIONS_URL, params=params)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= expected_min_total


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pos_id_key, source_enum",
    [
        ("system_pos_id", PositionSourceEnum.system),
        ("custom_pos_id", PositionSourceEnum.custom),
    ],
    ids=["get_single_system_position", "get_single_custom_position"],
)
async def test_get_position_by_id(
    client: AsyncClient,
    positions_test_data: dict,
    pos_id_key: str,
    source_enum: PositionSourceEnum,
):
    """
    Тест: Получение детальной информации о должности по ID.
    GET /positions/{position_id}

    Сценарий:
    1. Получаем ID существующей должности (системной или кастомной) из фикстуры.
    2. Отправляем запрос с указанием ID и источника.
    3. Проверяем, что вернулся объект с запрашиваемым ID.
    """
    position_id = positions_test_data[pos_id_key]

    response = await client.get(
        f"{POSITIONS_URL}/{position_id}",
        params={"position_source": source_enum.value},
    )

    assert response.status_code == 200
    assert response.json()["id"] == position_id


@pytest.mark.asyncio
async def test_create_custom_position(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Создание новой кастомной должности.
    POST /positions/

    Сценарий:
    1. В БД создаются пользователь (владелец) и права доступа.
    2. Формируем payload с заголовком и списком ID прав.
    3. Отправляем POST запрос на создание.
    4. Проверяем, что в ответе вернулись корректные данные и присвоенный ID.
    """
    owner = await UserFactory.create_async(session)
    perm = await PermissionFactory.create_async(session)

    payload = CustomPositionCreatePayloadFactory.build(
        owner_id=owner.id,
        permission_ids=[perm.id],
    ).model_dump(mode="json")

    response = await client.post(POSITIONS_URL, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["owner_id"] == payload["owner_id"]


@pytest.mark.asyncio
async def test_update_custom_position(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Обновление существующей кастомной должности.
    PATCH /positions/{position_id}

    Сценарий:
    1. В БД создаётся исходная кастомная должность.
    2. Формируем payload с новым заголовком и измененным списком прав.
    3. Отправляем PATCH запрос.
    4. Проверяем, что возвращённые данные соответствуют обновленным значениям.
    """
    user = await UserFactory.create_async(session)
    position = await CustomPositionFactory.create_async(session, owner_id=user.id)

    new_perm = await PermissionFactory.create_async(session)

    payload = CustomPositionUpdatePayloadFactory.build(
        title="Updated Title",
        permission_ids=[new_perm.id],
    ).model_dump(mode="json")

    response = await client.patch(f"{POSITIONS_URL}/{position.id}", json=payload)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_custom_position(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Удаление кастомной должности.
    DELETE /positions/{position_id}

    Сценарий:
    1. В БД создаётся кастомная должность.
    2. Отправляем DELETE запрос по ID должности.
    3. Проверяем статус ответа 204 No Content.
    4. Проверяем, что запись физически удалена из таблицы в БД.
    """
    user = await UserFactory.create_async(session)
    position = await CustomPositionFactory.create_async(session, owner_id=user.id)

    response = await client.delete(f"{POSITIONS_URL}/{position.id}")

    assert response.status_code == 204

    stmt = select(CustomPositions).where(CustomPositions.id == position.id)
    result = await session.execute(stmt)
    assert result.scalar_one_or_none() is None
