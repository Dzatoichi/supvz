import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Users
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
    "page, size",
    [(1, 10), (1, 1)],
    ids=["default_pagination", "small_page_size"],
)
async def test_get_users_list(
    client: AsyncClient,
    session: AsyncSession,
    page: int,
    size: int,
):
    """
    Тест: Получение списка пользователей с пагинацией.
    GET /users/

    Сценарий:
    1. В БД создаются несколько пользователей.
    2. Отправляем запрос с параметрами пагинации.
    3. Проверяем, что возвращается список и метаданные пагинации.
    """
    await UserFactory.create_async(session)
    await UserFactory.create_async(session)

    response = await client.get(USERS_URL, params={"page": page, "size": size})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 2
    assert len(data["items"]) <= size


@pytest.mark.asyncio
async def test_get_user_by_id(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Получение данных конкретного пользователя.
    GET /users/{user_id}

    Сценарий:
    1. Создаем пользователя в БД.
    2. Запрашиваем его по ID.
    3. Проверяем соответствие возвращенных данных.
    """
    user = await UserFactory.create_async(session)

    response = await client.get(f"{USERS_URL}/{user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email


@pytest.mark.asyncio
async def test_update_user(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Обновление данных пользователя (email).
    PATCH /users/{user_id}

    Сценарий:
    1. Создаем пользователя.
    2. Формируем payload с новым email.
    3. Отправляем PATCH запрос.
    4. Проверяем, что email обновился.
    """
    user = await UserFactory.create_async(session)
    new_email = "updated_email@example.com"

    payload = UserUpdatePayloadFactory.build(email=new_email).model_dump(mode="json")

    response = await client.patch(f"{USERS_URL}/{user.id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == new_email


@pytest.mark.asyncio
async def test_set_paid_sub(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Переключение подписки пользователя (test -> paid).
    POST /users/{user_id}/set_paid_sub

    Сценарий:
    1. Создаем пользователя со статусом подписки 'test'.
    2. Отправляем запрос на обновление подписки.
    3. Проверяем, что запрос прошел успешно.
    """
    user = await UserFactory.create_async(session)

    response = await client.post(f"{USERS_URL}/{user.id}/set_paid_sub")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["subscription"] == "paid"


@pytest.mark.asyncio
async def test_delete_user(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Удаление пользователя.
    DELETE /users/{user_id}

    Сценарий:
    1. Создаем пользователя.
    2. Отправляем запрос на удаление.
    3. Проверяем статус 204.
    4. Проверяем, что пользователь удален из БД.
    """
    user = await UserFactory.create_async(session)

    response = await client.delete(f"{USERS_URL}/{user.id}")

    assert response.status_code == 204

    stmt = select(Users).where(Users.id == user.id)
    result = await session.execute(stmt)
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_update_user_permissions(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Полная перезапись прав пользователя.
    PUT /users/{user_id}/permissions

    Сценарий:
    1. Создаем пользователя и два права доступа.
    2. Отправляем запрос со списком ID этих прав.
    3. Проверяем, что в ответе вернулся список присвоенных прав.
    """
    user = await UserFactory.create_async(session)
    perm1 = await PermissionFactory.create_async(session)
    perm2 = await PermissionFactory.create_async(session)

    payload = UpdateUserPermissionsPayloadFactory.build(permission_ids=[perm1.id, perm2.id]).model_dump(mode="json")

    response = await client.put(f"{USERS_URL}/{user.id}/permissions", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    returned_ids = [p["id"] for p in data]
    assert perm1.id in returned_ids
    assert perm2.id in returned_ids


@pytest.mark.asyncio
async def test_bulk_update_users_permissions(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Массовое обновление прав для нескольких пользователей.
    PUT /users/permissions/

    Сценарий:
    1. Создаем двух пользователей и право доступа.
    2. Формируем payload: список ID юзеров + список ID прав.
    3. Отправляем запрос на массовое обновление.
    4. Проверяем успешный статус ответа.
    """
    user1 = await UserFactory.create_async(session)
    user2 = await UserFactory.create_async(session)
    perm = await PermissionFactory.create_async(session)

    payload = UpdateUsersPermissionsPayloadFactory.build(
        users=[user1.id, user2.id], new_permission_ids=[perm.id]
    ).model_dump(mode="json")

    response = await client.put(f"{USERS_URL}/permissions/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_get_me_success(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Получение профиля текущего пользователя (GET /users/me).
    """
    user = await UserFactory.create_async(session)
    token = create_test_auth_token(user_id=user.id)
    client.cookies.set("access_token", token)

    response = await client.get(f"{USERS_URL}/me")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email
