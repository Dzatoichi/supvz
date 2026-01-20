import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.models.employees.employees import Employees
from src.tests.factories import EmployeeFactory, PVZFactory

pytestmark = pytest.mark.anyio

# ID тестового пользователя-владельца
TEST_OWNER_ID = 999999


@pytest.mark.asyncio
async def test_create_employee(client, session):
    """
    Тест: Успешное создание сотрудника.
    POST /employees
    """

    payload_model = EmployeeFactory.build()
    payload = payload_model.model_dump(mode="json", exclude={"id"})

    response = await client.post("/employees", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == payload["name"]


@pytest.mark.asyncio
async def test_get_employee_by_id(client, session):
    """
    Тест: Получение сотрудника по user_id.
    GET /employees/{user_id}
    """
    employee = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)

    response = await client.get(f"/employees/{employee.user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == employee.user_id


@pytest.mark.asyncio
async def test_get_employees_filtered(client, session, make_auth_headers):
    """
    Тест: Получение списка сотрудников с фильтрацией.
    GET /employees?user_id=...&pvz_id=...

    Сценарий:
    1. Создаем владельца (owner_id).
    2. Создаем 2 сотрудников, привязанных к этому владельцу.
    3. Создаем 3-го сотрудника ("шум") с другим владельцем.
    4. Проверяем, что фильтр по user_id (owner_id) возвращает только нужных.
    """

    target_owner_id = 100
    other_owner_id = 200

    target_employees = []
    for _ in range(2):
        emp = await EmployeeFactory.create_async(session, owner_id=target_owner_id)
        target_employees.append(emp)

    await EmployeeFactory.create_async(session, owner_id=other_owner_id)

    # Создаем клиент, авторизованный как target_owner_id,
    headers = make_auth_headers(target_owner_id)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as target_client:
        response = await target_client.get("/employees")

        assert response.status_code == 200
        data = response.json()

        assert "items" in data
        assert data["total"] == 2

        received_ids = {employee["user_id"] for employee in data["items"]}
        expected_ids = {e.user_id for e in target_employees}
        assert received_ids == expected_ids


@pytest.mark.asyncio
async def test_update_employee(client, session):
    """
    Тест: Обновление данных сотрудника.
    PATCH /employees/{user_id}
    """
    employee = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)

    update_payload = {"name": "Updated Name Ivanov", "phone_number": "+79990000000"}

    response = await client.patch(f"/employees/{employee.user_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_payload["name"]
    assert data["phone_number"] == update_payload["phone_number"]


@pytest.mark.asyncio
async def test_assign_employee_to_pvz(client, session):
    """
    Тест: Привязка сотрудника к ПВЗ (или перевод в другой).
    POST /employees/{user_id}/assign
    """
    employee = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)
    pvz = await PVZFactory.create_async(session, owner_id=TEST_OWNER_ID)

    payload = {"new_pvz_id": pvz.id}

    response = await client.post(f"/employees/{employee.user_id}/assign", json=payload)

    assert response.status_code == 200

    await session.refresh(employee, attribute_names=["pvzs"])
    assert len(employee.pvzs) == 1
    assert employee.pvzs[0].id == pvz.id


@pytest.mark.asyncio
async def test_unassign_employee_from_pvz(client, session):
    """
    Тест: Отвязка сотрудника от ПВЗ.
    DELETE /employees/{user_id}/unassign/{pvz_id}
    """
    employee = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)
    pvz = await PVZFactory.create_async(session, owner_id=TEST_OWNER_ID)

    await session.refresh(employee, attribute_names=["pvzs"])
    employee.pvzs.append(pvz)
    await session.flush()

    await session.refresh(employee, attribute_names=["pvzs"])
    assert len(employee.pvzs) == 1

    response = await client.delete(f"/employees/{employee.user_id}/unassign/{pvz.id}")

    assert response.status_code == 204

    session.expire(employee)
    await session.refresh(employee, attribute_names=["pvzs"])

    assert len(employee.pvzs) == 0


@pytest.mark.asyncio
async def test_delete_employee(client, session):
    """
    Тест: Удаление сотрудника.
    DELETE /employees/{user_id}
    """
    employee = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)
    user_id = employee.user_id

    response = await client.delete(f"/employees/{user_id}")

    assert response.status_code == 204

    deleted_emp = await session.get(Employees, user_id)
    assert deleted_emp is None
