import pytest
from sqlalchemy import select

from src.models.pvzs.PVZs import PVZs
from src.tests.factories import EmployeeFactory, GroupFactory, PVZFactory, PVZUpdateFactory

pytestmark = pytest.mark.anyio


@pytest.mark.asyncio
async def test_add_pvz(client, session):
    """
    Тест: Успешное создание ПВЗ.
    POST /pvzs/
    Проверяет корректность ответа API и сохранение внешних ключей (group_id).
    """

    group = await GroupFactory.create_async(session)

    pvz_payload = PVZFactory.build(
        code="TEST-CODE-001",
        group_id=group.id,
        owner_id=group.owner_id,
    )

    response = await client.post("/pvzs/", json=pvz_payload.model_dump(mode="json"))

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "TEST-CODE-001"
    assert data["group_id"] == group.id


@pytest.mark.asyncio
async def test_update_pvz_success(client, session):
    """
    Тест: Успешное обновление данных ПВЗ (PATCH).
    PATCH /pvzs/{pvz_id}
    Проверяет изменение полей и привязку к новым сущностям (группа, куратор).
    """

    pvz = await PVZFactory.create_async(session)
    group = await GroupFactory.create_async(session)

    pvz_update_payload = PVZUpdateFactory.build(
        address=pvz.address,
        owner_id=pvz.owner_id,
        curator_id=1,
        group_id=group.id,
    )

    response = await client.patch(f"/pvzs/{pvz.id}", json=pvz_update_payload.model_dump(mode="json"))

    assert response.status_code == 200
    data = response.json()
    assert data["curator_id"] == 1
    assert data["group_id"] == group.id


@pytest.mark.asyncio
async def test_get_pvz_by_id_success(client, session):
    """
    Тест: Получение одного ПВЗ по ID.
    GET /pvzs/{pvz_id}
    Проверяет соответствие возвращаемых данных созданным в БД.
    """

    pvz = await PVZFactory.create_async(session)

    response = await client.get(f"/pvzs/{pvz.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pvz.id
    assert data["code"] == pvz.code


@pytest.mark.asyncio
async def test_get_pvzs_with_query_params(client, session):
    """
    Тест: Фильтрация списка ПВЗ и пагинация.
    GET /pvzs/
    Проверяет, что фильтр по group_id возвращает только целевые записи
    и корректно считает total count.
    """

    target_group = await GroupFactory.create_async(session)

    target_pvzs = []
    for _ in range(3):
        pvz = await PVZFactory.create_async(session, group_id=target_group.id)
        target_pvzs.append(pvz)

    for _ in range(7):
        await PVZFactory.create_async(session)

    response = await client.get("/pvzs/", params={"group_id": target_group.id})

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert "total" in data

    assert data["total"] == 3
    assert len(data["items"]) == 3

    received_ids = [item["id"] for item in data["items"]]
    target_ids = [p.id for p in target_pvzs]

    assert set(received_ids) == set(target_ids)


@pytest.mark.asyncio
async def test_delete_pvz_success(client, session):
    """
    Тест: Удаление ПВЗ.
    DELETE /pvzs/{pvz_id}
    Проверяет статус ответа API и физическое отсутствие записи в БД после удаления.
    """

    pvz = await PVZFactory.create_async(session)

    pvz_id = pvz.id

    response = await client.delete(f"/pvzs/{pvz_id}")

    assert response.status_code == 200
    assert response.json()["id"] == pvz_id

    deleted_pvz = await session.get(PVZs, pvz_id)
    assert deleted_pvz is None, "ПВЗ не удалился из БД"


@pytest.mark.asyncio
async def test_get_employees_success(client, session):
    """
    Тест: Получение списка сотрудников, привязанных к конкретному ПВЗ.
    GET /pvzs/{pvz_id}/employees
    Проверяет корректность работы Many-to-Many связей.
    """

    pvz = await PVZFactory.create_async(session)

    await session.refresh(pvz, attribute_names=["employees"])

    id_in_pvz = None
    target_employees = []
    for _ in range(3):
        employee = await EmployeeFactory.create_async(session)
        target_employees.append(employee)
        id_in_pvz = employee.user_id

        pvz.employees.append(employee)

    noise_emp = await EmployeeFactory.create_async(session)

    await session.flush()

    response = await client.get(f"/pvzs/{pvz.id}/employees", params={"user_id": id_in_pvz})

    assert response.status_code == 200
    data = response.json()

    items = data["items"] if "items" in data else data
    assert len(items) == 3

    received_ids = {employee["user_id"] for employee in items}
    assert noise_emp.user_id not in received_ids


@pytest.mark.asyncio
async def test_assign_pvz_to_group_success(client, session):
    """
    Тест: Массовая привязка ПВЗ к группе.
    PATCH /pvzs/group_assignment
    Проверяет обновление group_id у списка переданных ПВЗ.
    """

    target_group = await GroupFactory.create_async(session, owner_id=1)

    pvz_ids = []
    for _ in range(5):
        pvz = await PVZFactory.create_async(
            session,
            owner_id=target_group.owner_id,
        )
        await PVZFactory.create_async(session)

        pvz_ids.append(pvz.id)

    payload = {
        "group_id": target_group.id,
        "pvz_ids": pvz_ids,
    }

    response = await client.patch("/pvzs/group_assignment", json=payload)

    assert response.status_code == 200

    stmt = select(PVZs).where(PVZs.id.in_(pvz_ids))
    result = await session.execute(stmt)
    updated_pvzs = result.scalars().all()

    assert len(updated_pvzs) == 5

    for pvz in updated_pvzs:
        assert pvz.group_id == target_group.id
