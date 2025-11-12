import pytest

pytestmark = pytest.mark.anyio


async def test_get_non_existent_pvz_by_id(client):
    """
    Тест: GET /pvzs/{pvz_id} должен вернуть 404, если ПВЗ не найден.
    """
    response = await client.get("/pvzs/999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Pvz not found"


async def test_add_pvz_with_conflicting_code(client):
    """
    Тест: POST /pvzs/ должен вернуть 409, если код ПВЗ уже существует.
    """
    conflicting_pvz_data = {
        "code": "EXISTING-CODE",
        "type": "ozon",
        "address": "Some Address",
        "group_id": 0,
        "owner_id": 1,
        "curator_id": 1,
    }

    response = await client.post("/pvzs/", json=conflicting_pvz_data)

    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Pvz already exists"


async def test_update_non_existent_pvz(client):
    """
    Тест: PATCH /pvzs/{pvz_id} должен вернуть 404, если ПВЗ не найден.
    """
    update_data = {
        "address": "some new address",
        "owner_id": 1,
        "curator_id": 1,
        "group": "A",
    }

    response = await client.patch("/pvzs/999", json=update_data)

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Pvz not found"


async def test_delete_non_existent_pvz_by_id(client):
    """
    Тест: DELETE /pvzs/{pvz_id} должен вернуть 404, если ПВЗ не найден.
    """
    response = await client.delete("/pvzs/999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Pvz not found"


async def test_add_pvz_with_invalid_data(client):
    """
    Тест: POST /pvzs/ должен вернуть 422, если данные невалидны.
    Это проверка встроенной валидации FastAPI/Pydantic.
    """
    invalid_data = {
        "code": "VALID-CODE",
        "type": "ozon",
        "address": "Some Address",
        "group": "A",
        "owner_id": "не число",
        "curator_id": 1,
    }

    response = await client.post("/pvzs/", json=invalid_data)

    assert response.status_code == 422
    data = response.json()
    # проверяем, что в сообщениях есть про integer
    assert any("integer" in msg for msg in data["detail"])
