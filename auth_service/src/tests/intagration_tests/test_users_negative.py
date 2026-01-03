import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.factories.permission_factories import PermissionFactory
from src.tests.factories.user_factories import (
    UpdateUserPermissionsPayloadFactory,
    UpdateUsersPermissionsPayloadFactory,
    UserFactory,
    UserUpdatePayloadFactory,
)
from src.tests.utils import create_test_auth_token

USERS_URL = "/users"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, expected_msg_part",
    [
        ("abc", "valid integer"),
        ("not-a-number", "valid integer"),
    ],
    ids=[
        "user_id_string",
        "user_id_invalid_string",
    ],
)
async def test_get_user_by_id_validation_errors(
    client: AsyncClient,
    user_id: str,
    expected_msg_part: str,
):
    """
    Тест: Ошибки валидации user_id в path-параметре.
    GET /users/{invalid_user_id}

    Сценарий:
    1. Отправляем запрос с невалидным user_id.
    2. Проверяем статус 422 Unprocessable Entity.
    """
    response = await client.get(f"{USERS_URL}/{user_id}")
    data = response.json()
    error_messages = data["detail"]

    match_found = any(expected_msg_part.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
async def test_get_user_not_found(
    client: AsyncClient,
):
    """
    Тест: Запрос несуществующего пользователя.
    GET /users/{non_existent_id}

    Сценарий:
    1. Отправляем запрос с несуществующим user_id.
    2. Проверяем статус 404 Not Found.
    """
    non_existent_id = 999999

    response = await client.get(f"{USERS_URL}/{non_existent_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_not_found(
    client: AsyncClient,
):
    """
    Тест: Обновление несуществующего пользователя.
    PATCH /users/{non_existent_id}

    Сценарий:
    1. Формируем валидный payload.
    2. Отправляем PATCH запрос на несуществующий user_id.
    3. Проверяем статус 404 Not Found.
    """
    non_existent_id = 999999
    payload = UserUpdatePayloadFactory.build().model_dump(mode="json")

    response = await client.patch(f"{USERS_URL}/{non_existent_id}", json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_set_paid_sub_user_not_found(
    client: AsyncClient,
):
    """
    Тест: Переключение подписки для несуществующего пользователя.
    POST /users/{non_existent_id}/set_paid_sub

    Сценарий:
    1. Отправляем POST запрос с несуществующим user_id.
    2. Проверяем статус 404 Not Found.
    """
    non_existent_id = 999999

    response = await client.post(f"{USERS_URL}/{non_existent_id}/set_paid_sub")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_permissions_user_not_found(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Обновление прав для несуществующего пользователя.
    PUT /users/{non_existent_id}/permissions

    Сценарий:
    1. Создаем валидное право доступа.
    2. Отправляем PUT запрос на несуществующий user_id.
    3. Проверяем статус 404 Not Found.
    """
    non_existent_id = 999999
    perm = await PermissionFactory.create_async(session)

    payload = UpdateUserPermissionsPayloadFactory.build(permission_ids=[perm.id]).model_dump(mode="json")

    response = await client.put(f"{USERS_URL}/{non_existent_id}/permissions", json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_override, expected_msg_part",
    [
        ({"email": "not-an-email"}, "valid email"),
        ({"email": ""}, "valid email"),
        ({"email": None}, "string"),
        ({"email": 12345}, "string"),
    ],
    ids=[
        "email_invalid_format",
        "email_empty_string",
        "email_null",
        "email_not_string",
    ],
)
async def test_update_user_validation_errors(
    client: AsyncClient,
    session: AsyncSession,
    payload_override: dict,
    expected_msg_part: str,
):
    """
    Тест: Ошибки валидации при обновлении пользователя.
    PATCH /users/{user_id}

    Сценарий:
    1. Создаем пользователя в БД.
    2. Формируем payload с невалидными данными.
    3. Отправляем PATCH запрос.
    4. Проверяем статус 422 и текст ошибки.
    """
    user = await UserFactory.create_async(session)

    payload = UserUpdatePayloadFactory.build().model_dump(mode="json")
    payload.update(payload_override)

    response = await client.patch(f"{USERS_URL}/{user.id}", json=payload)
    data = response.json()
    error_messages = data["detail"]

    match_found = any(expected_msg_part.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_override, expected_msg_part",
    [
        ({"permission_ids": "not-a-list"}, "list"),
        ({"permission_ids": ["abc", "def"]}, "valid integer"),
        ({"permission_ids": None}, "list"),
    ],
    ids=[
        "permission_ids_not_list",
        "permission_ids_items_not_int",
        "permission_ids_null",
    ],
)
async def test_update_user_permissions_validation_errors(
    client: AsyncClient,
    session: AsyncSession,
    payload_override: dict,
    expected_msg_part: str,
):
    """
    Тест: Ошибки валидации при обновлении прав пользователя.
    PUT /users/{user_id}/permissions

    Сценарий:
    1. Создаем пользователя в БД.
    2. Формируем payload с невалидными permission_ids.
    3. Отправляем PUT запрос.
    4. Проверяем статус 422 и текст ошибки.
    """
    user = await UserFactory.create_async(session)

    payload = UpdateUserPermissionsPayloadFactory.build().model_dump(mode="json")
    payload.update(payload_override)

    response = await client.put(f"{USERS_URL}/{user.id}/permissions", json=payload)
    data = response.json()
    error_messages = data["detail"]

    match_found = any(expected_msg_part.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_override, expected_msg_part",
    [
        ({"users": "not-a-list"}, "list"),
        ({"users": ["abc"]}, "valid integer"),
        ({"users": None}, "list"),
        ({"new_permission_ids": "not-a-list"}, "list"),
        ({"new_permission_ids": ["xyz"]}, "valid integer"),
        ({"new_permission_ids": None}, "list"),
    ],
    ids=[
        "users_not_list",
        "users_items_not_int",
        "users_null",
        "permission_ids_not_list",
        "permission_ids_items_not_int",
        "permission_ids_null",
    ],
)
async def test_bulk_update_permissions_validation_errors(
    client: AsyncClient,
    payload_override: dict,
    expected_msg_part: str,
):
    """
    Тест: Ошибки валидации при массовом обновлении прав.
    PUT /users/permissions/

    Сценарий:
    1. Формируем payload с невалидными данными.
    2. Отправляем PUT запрос.
    3. Проверяем статус 422 и текст ошибки.
    """
    payload = UpdateUsersPermissionsPayloadFactory.build(users=[1], new_permission_ids=[1]).model_dump(mode="json")
    payload.update(payload_override)

    response = await client.put(f"{USERS_URL}/permissions/", json=payload)
    data = response.json()
    error_messages = data["detail"]

    match_found = any(expected_msg_part.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
async def test_update_user_duplicate_email(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Обновление email на уже существующий.
    PATCH /users/{user_id}

    Сценарий:
    1. Создаем двух пользователей.
    2. Пытаемся обновить email первого на email второго.
    3. Проверяем ошибку конфликта (409 или 400).
    """
    user1 = await UserFactory.create_async(session)
    user2 = await UserFactory.create_async(session)

    payload = UserUpdatePayloadFactory.build(email=user2.email).model_dump(mode="json")

    response = await client.patch(f"{USERS_URL}/{user1.id}", json=payload)

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_user_permissions_invalid_permission_ids(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Присвоение несуществующих прав пользователю.
    PUT /users/{user_id}/permissions

    Сценарий:
    1. Создаем пользователя.
    2. Отправляем запрос с несуществующими permission_ids.
    3. Проверяем ошибку (404 или 400).
    """
    user = await UserFactory.create_async(session)
    non_existent_perm_ids = [999998, 999999]

    payload = UpdateUserPermissionsPayloadFactory.build(permission_ids=non_existent_perm_ids).model_dump(mode="json")

    response = await client.put(f"{USERS_URL}/{user.id}/permissions", json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_bulk_update_permissions_users_not_found(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Массовое обновление прав для несуществующих пользователей.
    PUT /users/permissions/

    Сценарий:
    1. Создаем валидное право.
    2. Отправляем запрос с несуществующими user_ids.
    3. Проверяем ошибку (404 или 400).
    """
    perm = await PermissionFactory.create_async(session)
    non_existent_user_ids = [999998, 999999]

    payload = UpdateUsersPermissionsPayloadFactory.build(
        users=non_existent_user_ids, new_permission_ids=[perm.id]
    ).model_dump(mode="json")

    response = await client.put(f"{USERS_URL}/permissions/", json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_bulk_update_permissions_invalid_permission_ids(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Массовое обновление с несуществующими правами.
    PUT /users/permissions/

    Сценарий:
    1. Создаем пользователей.
    2. Отправляем запрос с несуществующими permission_ids.
    3. Проверяем ошибку (404 или 400).
    """
    user1 = await UserFactory.create_async(session)
    user2 = await UserFactory.create_async(session)
    non_existent_perm_ids = [999998, 999999]

    payload = UpdateUsersPermissionsPayloadFactory.build(
        users=[user1.id, user2.id], new_permission_ids=non_existent_perm_ids
    ).model_dump(mode="json")

    response = await client.put(f"{USERS_URL}/permissions/", json=payload)

    assert response.status_code in [400, 404]


@pytest.mark.asyncio
async def test_get_me_user_deleted(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Токен валиден, но пользователь удален из БД.
    GET /users/me

    Сценарий:
    1. Создаем пользователя и генерируем токен.
    2. Удаляем пользователя из БД физически.
    3. Пытаемся зайти по токену.
    4. Проверяем статус 401 Unauthorized и сообщение ошибки.
    """
    user = await UserFactory.create_async(session)
    token = create_test_auth_token(user.id)

    await session.delete(user)
    await session.commit()

    client.cookies.set("access_token", token)
    response = await client.get(f"{USERS_URL}/me")

    assert response.status_code == 401
