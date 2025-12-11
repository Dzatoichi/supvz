import pytest

from src.tests.factories import GroupFactory

pytestmark = pytest.mark.anyio


@pytest.mark.asyncio
async def test_create_group_validation_error(client):
    """
    Тест: Ошибка валидации при создании группы (422).
    Проверяет, что нельзя создать группу без обязательного поля owner_id.
    """
    invalid_payload = {}

    response = await client.post("/pvz_groups", json=invalid_payload)

    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"] == "validation_error"


@pytest.mark.asyncio
async def test_create_group_duplicate_name(client, session):
    """
    Тест: Создание группы с неуникальным именем (409 Conflict).
    Проверяет constraint unique=True поля name.
    """
    existing_name = "Unique Group Name"

    await GroupFactory.create_async(session, name=existing_name)

    payload_model = GroupFactory.build(name=existing_name)
    payload = payload_model.model_dump(mode="json")

    response = await client.post("/pvz_groups", json=payload)

    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Группа с таким именем уже существет"


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
    assert response.json()["error"] == "not_found"


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
    assert data["error"] == "validation_error"


@pytest.mark.asyncio
async def test_assign_curator_group_not_found(client):
    """
    Тест: Назначение куратора несуществующей группе (404).
    PATCH /pvz_groups/{group_id}/curator
    """
    non_existent_id = 999999

    response = await client.patch(f"/pvz_groups/{non_existent_id}/curator", params={"curator_id": 1})

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
