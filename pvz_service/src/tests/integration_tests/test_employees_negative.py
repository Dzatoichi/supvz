import pytest

from src.tests.factories import TEST_OWNER_ID, EmployeeFactory, PVZFactory

pytestmark = pytest.mark.anyio

NON_EXISTENT_ID = 777777


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, error_field",
    [
        ({}, "required"),
        ({"name": "a" * 256}, "at most 255 characters"),
        ({"phone_number": "not-a-number"}, "phone"),
    ],
)
async def test_create_employee_validation_error(client, payload, error_field):
    """
    Тест: Ошибка валидации при создании сотрудника (422).
    POST /employees
    """
    base_payload = EmployeeFactory.build().model_dump()
    base_payload.update(payload)

    final_payload = payload if payload == {} else base_payload

    response = await client.post("/employees", json=final_payload)

    assert response.status_code == 422

    data = response.json()
    error_messages = data["detail"]

    match_found = any(error_field.lower() in msg.lower() for msg in error_messages)

    assert match_found


@pytest.mark.asyncio
async def test_get_employee_not_found(client):
    """
    Тест: Получение несуществующего сотрудника (404).
    GET /employees/{user_id}
    """
    non_existent_id = 999999

    response = await client.get(f"/employees/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["error"] == "employee_not_found"


@pytest.mark.asyncio
async def test_update_employee_not_found(client):
    """
    Тест: Обновление несуществующего сотрудника (404).
    PATCH /employees/{user_id}
    """
    update_payload = {"name": "Ghost"}

    response = await client.patch(f"/employees/{NON_EXISTENT_ID}", json=update_payload)

    assert response.status_code == 404
    assert response.json()["error"] == "employee_not_found"


@pytest.mark.asyncio
async def test_assign_employee_not_found(client, session):
    """
    Тест: Привязка несуществующего сотрудника к ПВЗ (404).
    POST /employees/{user_id}/assign
    """
    non_existent_user_id = 999999
    pvz = await PVZFactory.create_async(session)

    payload = {"new_pvz_id": pvz.id}

    response = await client.post(f"/employees/{non_existent_user_id}/assign", json=payload)

    assert response.status_code == 404
    assert response.json()["error"] == "employee_not_found"


@pytest.mark.asyncio
async def test_assign_employee_to_non_existent_pvz(client, session):
    """
    Тест: Привязка сотрудника к несуществующему ПВЗ (404).
    POST /employees/{user_id}/assign
    """
    employee = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)
    non_existent_pvz_id = 999999

    payload = {"new_pvz_id": non_existent_pvz_id}

    response = await client.post(f"/employees/{employee.user_id}/assign", json=payload)

    assert response.status_code == 404
    assert response.json()["error"] == "pvz_not_found"


@pytest.mark.asyncio
async def test_unassign_employee_not_found(client, session):
    """
    Тест: Отвязка несуществующего сотрудника (404).
    DELETE /employees/{user_id}/unassign/{pvz_id}
    """
    non_existent_user_id = 999999
    pvz = await PVZFactory.create_async(session)

    response = await client.delete(f"/employees/{non_existent_user_id}/unassign/{pvz.id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_employee_not_found(client):
    """
    Тест: Удаление несуществующего сотрудника (404).
    DELETE /employees/{user_id}
    """
    non_existent_id = 999999

    response = await client.delete(f"/employees/{non_existent_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_assign_employee_duplicate_conflict(client, session):
    """
    Тест: Повторная привязка сотрудника к тому же ПВЗ (409 Conflict).
    POST /employees/{user_id}/assign
    """
    employee = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)
    pvz = await PVZFactory.create_async(session, owner_id=TEST_OWNER_ID)

    await session.refresh(employee, attribute_names=["pvzs"])
    employee.pvzs.append(pvz)
    await session.flush()

    payload = {"new_pvz_id": pvz.id}
    response = await client.post(f"/employees/{employee.user_id}/assign", json=payload)

    assert response.status_code == 409
