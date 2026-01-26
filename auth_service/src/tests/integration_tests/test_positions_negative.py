import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.enums import PositionSourceEnum
from src.tests.factories.custom_position_factories import (
    CustomPositionCreatePayloadFactory,
    CustomPositionFactory,
    CustomPositionUpdatePayloadFactory,
)
from src.tests.factories.user_factories import UserFactory

POSITIONS_URL = "/positions"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, expected_msg_part",
    [
        ({"position_source": "invalid_source"}, "Input should be 'system' or 'custom'"),
        ({"owner_id": "abc", "position_source": "custom"}, "valid integer"),
        ({}, "field required"),
    ],
    ids=[
        "invalid_source_enum",
        "invalid_owner_id_type",
        "missing_source_param",
    ],
)
async def test_get_positions_validation_errors(
    client: AsyncClient,
    params: dict,
    expected_msg_part: str,
):
    """
    Тест: Ошибки валидации параметров списка должностей.
    GET /positions/?{invalid_params}

    Сценарий:
    1. Отправляем запрос с некорректными query-параметрами.
    2. Проверяем статус 422 Unprocessable Entity.
    3. Проверяем наличие ожидаемого текста ошибки в теле ответа.
    """
    response = await client.get(POSITIONS_URL, params=params)

    assert response.status_code == 422
    data = response.json()
    error_messages = data["detail"]

    match_found = any(expected_msg_part.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_override, expected_msg_part",
    [
        ({"title": None}, "string"),
        ({"title": ""}, "string"),
        ({"owner_id": "string"}, "valid integer"),
        ({"owner_id": None}, "valid integer"),
        ({"permission_ids": "not-list"}, "list"),
        ({"permission_ids": ["abc"]}, "valid integer"),
    ],
    ids=[
        "title_none",
        "title_empty",
        "owner_id_string",
        "owner_id_none",
        "permissions_not_list",
        "permissions_items_not_int",
    ],
)
async def test_create_position_validation_errors(
    client: AsyncClient,
    payload_override: dict,
    expected_msg_part: str,
):
    """
    Тест: Ошибки валидации тела запроса при создании.
    POST /positions/

    Сценарий:
    1. Генерируем валидный payload через фабрику.
    2. Подменяем поля на невалидные значения.
    3. Отправляем POST запрос.
    4. Проверяем статус 422 и текст ошибки.
    """
    base_payload = CustomPositionCreatePayloadFactory.build().model_dump(mode="json")
    base_payload.update(payload_override)

    response = await client.post(POSITIONS_URL, json=base_payload)

    assert response.status_code == 422
    data = response.json()
    error_messages = data["detail"]

    match_found = any(expected_msg_part.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
async def test_get_position_not_found(
    client: AsyncClient,
):
    """
    Тест: Запрос несуществующей должности.
    GET /positions/{non_existent_id}

    Сценарий:
    1. Отправляем запрос с заведомо несуществующим ID.
    2. Проверяем, что возвращается статус 404 Not Found.
    """
    non_existent_id = 999999

    response = await client.get(
        f"{POSITIONS_URL}/{non_existent_id}",
        params={"position_source": PositionSourceEnum.custom.value},
    )

    assert response.status_code == 404
    assert response.json()["error"] == "position_not_found"


@pytest.mark.asyncio
async def test_update_position_not_found(
    client: AsyncClient,
):
    """
    Тест: Обновление несуществующей должности.
    PATCH /positions/{non_existent_id}

    Сценарий:
    1. Генерируем валидный payload обновления.
    2. Отправляем PATCH запрос на несуществующий ID.
    3. Проверяем статус 404 Not Found.
    """
    non_existent_id = 999999
    payload = CustomPositionUpdatePayloadFactory.build().model_dump(mode="json")

    response = await client.patch(f"{POSITIONS_URL}{non_existent_id}", json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_position_not_found(
    client: AsyncClient,
):
    """
    Тест: Удаление несуществующей должности.
    DELETE /positions/{non_existent_id}

    Сценарий:
    1. Отправляем DELETE запрос на несуществующий ID.
    2. Проверяем статус 204.
    """
    non_existent_id = 999999

    response = await client.delete(f"{POSITIONS_URL}/{non_existent_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_create_position_user_not_found(
    client: AsyncClient,
):
    """
    Тест: Создание должности для несуществующего владельца.
    POST /positions/

    Сценарий:
    1. Формируем payload с несуществующим owner_id.
    2. Отправляем POST запрос.
    3. Проверяем, что сервис возвращает ошибку (обычно 404 UserNotFound).
    """
    non_existent_user_id = 999999
    payload = CustomPositionCreatePayloadFactory.build(owner_id=non_existent_user_id).model_dump(mode="json")

    response = await client.post(POSITIONS_URL, json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_position_duplicate_title(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Создание должности с дублирующимся названием у одного владельца.
    POST /positions/

    Сценарий:
    1. Создаем пользователя и одну должность в БД.
    2. Пытаемся создать вторую должность с ТЕМ ЖЕ названием и ТЕМ ЖЕ владельцем.
    3. Проверяем, что возвращается ошибка конфликта (409 Conflict).
    """
    user = await UserFactory.create_async(session)
    await CustomPositionFactory.create_async(session, owner_id=user.id, title="Unique Manager")

    payload = CustomPositionCreatePayloadFactory.build(
        owner_id=user.id,
        title="Unique Manager",
    ).model_dump(mode="json")

    response = await client.post(POSITIONS_URL, json=payload)

    assert response.status_code == 409
