import pytest

from src.tests.factories import PVZFactory

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
    assert data["detail"] == "ПВЗ с таким id не найдено"


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
    await PVZFactory.create_async(session, code=existing_code)

    new_pvz_payload = PVZFactory.build(code=existing_code)

    response = await client.post("/pvzs/", json=new_pvz_payload.model_dump(mode="json"))

    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "ПВЗ с таким кодом уже существует"


@pytest.mark.asyncio
async def test_create_pvz_validation_error(client):
    """
    Тест: Ошибка валидации данных (422 Unprocessable Entity).
    GET /pvzs/{pvz_id}/employees
    Проверяет реакцию на отсутствие обязательных полей.
    """
    invalid_payload = {}

    response = await client.post("/pvzs/", json=invalid_payload)

    assert response.status_code == 422
    data = response.json()
    assert "Field required" in data["detail"]


@pytest.mark.asyncio
async def test_create_pvz_invalid_types(client):
    """
    Тест: Ошибка типов данных (422).
    PATCH /pvzs/group_assignment
    Проверяет, что нельзя передать строку туда, где ожидается число.
    """
    payload = {
        "code": "TEST",
        "type": "ozon",
        "address": "Test Addr",
        "owner_id": "NOT-A-NUMBER",
        "group_id": 1,
    }

    response = await client.post("/pvzs/", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"] == ["Input should be a valid integer, unable to parse string as an integer"]


@pytest.mark.asyncio
async def test_get_employees_pvz_not_found(client):
    """
    Тест: Получение сотрудников для несуществующего ПВЗ (404).
    """
    non_existent_id = 999999

    response = await client.get(f"/pvzs/{non_existent_id}/employees", params={"user_id": non_existent_id})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_assign_group_not_found(client, session):
    """
    Тест: Привязка ПВЗ к несуществующей группе (404).
    """
    # Создаем ПВЗ, чтобы pvz_ids были валидными
    pvz = await PVZFactory.create_async(session)
    non_existent_group_id = 999999

    payload = {"group_id": non_existent_group_id, "pvz_ids": [pvz.id]}

    response = await client.patch("/pvzs/group_assignment", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Группа не найдена"
