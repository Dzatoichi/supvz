import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.tests.factories import GroupFactory

pytestmark = pytest.mark.anyio


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, error_field",
    [
        ({}, "required"),
        ({"responsible_id": "boss"}, "valid integer"),
        ({"name": None}, "string"),
    ],
)
async def test_create_group_validation_error(client, payload, error_field):
    """
    Тест: Ошибка валидации при создании группы (422).
    POST /pvz_groups
    """
    base_payload = GroupFactory.build().model_dump()
    base_payload.update(payload)

    final_payload = payload if payload == {} else base_payload

    response = await client.post("/pvz_groups", json=final_payload)

    assert response.status_code == 422

    data = response.json()
    error_messages = data["detail"]

    match_found = any(error_field.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
async def test_create_group_duplicate(session, make_auth_headers):
    """
    Тест: Создание группы с неуникальным именем (409 Conflict).
    Сценарий:
    1. Создаем группу для пользователя user_id=100.
    2. Авторизуемся как user_id=100.
    3. Пытаемся создать группу с тем же именем.
    4. Ожидаем 409.
    """
    target_owner_id = 100
    duplicate_name = "Unique Group Name"

    await GroupFactory.create_async(session, name=duplicate_name, owner_id=target_owner_id)

    payload = {"name": duplicate_name}

    headers = make_auth_headers(target_owner_id)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as ac:
        response = await ac.post("/pvz_groups", json=payload)

        assert response.status_code == 409
        data = response.json()
        assert data["detail"] == "Группа с таким именем уже существует"


@pytest.mark.asyncio
async def test_get_group_not_found(client):
    """
    Тест: Получение несуществующей группы (404).
    GET /pvz_groups/{group_id}
    """
    non_existent_id = 999999

    response = await client.get(f"/pvz_groups/{non_existent_id}")

    assert response.status_code == 404
    # Проверь точный текст ошибки в своем сервисе
    assert response.json()["error"] == "pvz_group_not_found"


@pytest.mark.asyncio
async def test_update_group_not_found(client):
    """
    Тест: Обновление несуществующей группы (404).
    PATCH /pvz_groups/{group_id}
    """
    non_existent_id = 999999
    update_payload = {"name": "New Name"}

    response = await client.patch(f"/pvz_groups/{non_existent_id}", json=update_payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_group_conflict_name(client, session):
    """
    Тест: Обновление имени группы на уже занятое (409 Conflict).
    Сценарий: Группа А меняет имя на имя Группы Б.
    """
    await GroupFactory.create_async(session, name="Group A")
    group = await GroupFactory.create_async(session, name="Group B")

    update_payload = {"name": "Group A"}

    response = await client.patch(f"/pvz_groups/{group.id}", json=update_payload)

    assert response.status_code == 409
    data = response.json()
    assert data["error"] == "pvz_group_already_exists"


@pytest.mark.asyncio
async def test_assign_responsible_group_not_found(client):
    """
    Тест: Назначение куратора несуществующей группе (404).
    PATCH /pvz_groups/{group_id}/responsible
    """
    non_existent_id = 999999

    response = await client.patch(f"/pvz_groups/{non_existent_id}/responsible", params={"responsible_id": 1})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_group_not_found(client):
    """
    Тест: Удаление несуществующей группы (404).
    DELETE /pvz_groups/{group_id}
    """
    non_existent_id = 999999

    response = await client.delete(f"/pvz_groups/{non_existent_id}")

    assert response.status_code == 404
