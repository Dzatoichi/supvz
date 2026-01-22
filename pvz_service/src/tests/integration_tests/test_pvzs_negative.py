import pytest

from src.tests.conftest import TEST_OWNER_ID
from src.tests.factories import EmployeeFactory, PVZFactory

pytestmark = pytest.mark.anyio


@pytest.mark.asyncio
async def test_get_pvz_not_found(client):
    """
    Тест: Получение несуществующего ПВЗ (404).
    GET /pvzs/{pvz_id}
    Проверяет, что API возвращает корректную ошибку, если ID не найден.
    """
    non_existent_id = 999999

    response = await client.get(f"/pvzs/{non_existent_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "pvz_not_found"


@pytest.mark.asyncio
async def test_update_pvz_not_found(client):
    """
    Тест: Обновление несуществующего ПВЗ (404).
    PATCH /pvzs/{pvz_id}
    """
    non_existent_id = 999999
    update_data = {
        "address": "Nowhere",
        "owner_id": "123",
    }

    response = await client.patch(f"/pvzs/{non_existent_id}", json=update_data)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_pvz_not_found(client):
    """
    Тест: Удаление несуществующего ПВЗ (404).
    DELETE /pvzs/{pvz_id}
    """
    non_existent_id = 999999

    response = await client.delete(f"/pvzs/{non_existent_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_pvz_duplicate_code(client, session):
    """
    Тест: Создание ПВЗ с уже существующим кодом (409 Conflict).
    POST /pvzs/
    Проверяет уникальность поля 'code'.
    """
    existing_code = "DUPLICATE-CODE"

    await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID, user_id=TEST_OWNER_ID)
    await PVZFactory.create_async(session, code=existing_code)

    new_pvz_payload = PVZFactory.build(code=existing_code)

    response = await client.post("/pvzs/", json=new_pvz_payload.model_dump(mode="json"))

    assert response.status_code == 409
    data = response.json()
    assert data["error"] == "pvz_already_exists"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, error_field",
    [
        ({}, "required"),
        ({"type": "dhl"}, "input should be"),
        ({"responsible_id": "not-a-number"}, "valid integer"),
        ({"code": None}, "string"),
    ],
)
async def test_create_pvz_validation_error(client, payload, error_field):
    """
    Тест: Ошибка валидации данных (422 Unprocessable Entity).
    GET /pvzs/{pvz_id}/employees
    """
    base_payload = PVZFactory.build().model_dump(mode="json")
    base_payload.update(payload)

    final_payload = payload if payload == {} else base_payload

    response = await client.post("/pvzs/", json=final_payload)

    data = response.json()
    error_messages = data["detail"]

    match_found = any(error_field.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
async def test_get_employees_pvz_not_found(client):
    """
    Тест: Получение сотрудников для несуществующего ПВЗ (404).
    """
    non_existent_id = 999999

    response = await client.get(f"/pvzs/{non_existent_id}/employees", params={"user_id": non_existent_id})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_assign_pvz_to_group_not_found(client, session):
    """
    Тест: Привязка ПВЗ к несуществующей группе (404).
    """
    pvz = await PVZFactory.create_async(session)
    non_existent_group_id = 999999

    payload = {"group_id": non_existent_group_id, "pvz_ids": [pvz.id]}

    response = await client.patch("/pvzs/group_assignment", json=payload)

    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "pvz_group_not_found"
