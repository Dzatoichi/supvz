import pytest

pytestmark = pytest.mark.anyio


async def test_add_pvz(client):
    """
    Тестируем эндпоинт POST /pvzs/
    """
    pvz_data_to_create = {
        "code": "API-TEST-PVZ",
        "type": "ozon",
        "address": "123 Test Street",
        "group": "B",
        "owner_id": 5,
        "curator_id": 15,
    }

    response = await client.post("/pvzs/", json=pvz_data_to_create)

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == "API-TEST-PVZ"
    assert data["address"] == "123 Test Street"


async def test_get_pvz_by_id(client):
    """
    Тестируем эндпоинт GET /pvzs/{pvz_id}
    """
    response = await client.get("/pvzs/123")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 123
    assert data["code"] == "FETCHED-PVZ"


async def test_get_pvzs_with_query_params(client):
    """
    Тестируем эндпоинт GET /pvzs/ с query-параметрами
    """
    response = await client.get("/pvzs/", params={"code": "SOME-CODE", "group": "C"})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_update_pvz(client):
    """
    Тестируем эндпоинт PATCH /pvzs/{id} для обновления данных
    """
    update_data = {"address": "Новый обновленный адрес", "owner_id": 99, "curator_id": 88, "group": "Z"}

    response = await client.patch("/pvzs/123", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "FETCHED-PVZ-UPDATED"
    assert data["address"] == "Fetched Address_1"


async def test_delete_pvz_by_id(client):
    """
    Тестируем эндпоинт DELETE /pvzs/{id} для удаления данных
    """
    response = await client.delete("/pvzs/123")

    assert response.status_code == 200
