import pytest
from sqlalchemy import select

from src.models.pvzs.PVZGroups import PVZGroups
from src.models.pvzs.PVZs import PVZs
from src.tests.factories import EmployeeFactory, GroupFactory, PVZFactory

pytestmark = pytest.mark.anyio

TEST_OWNER_ID = 999999


@pytest.mark.asyncio
async def test_create_group(client, session):
    """
    Тест: Успешное создание группы ПВЗ.
    POST /pvz_groups/
    """

    await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID, user_id=TEST_OWNER_ID)

    payload_model = GroupFactory.build(owner_id=TEST_OWNER_ID, responsible_id=None)
    payload = payload_model.model_dump(mode="json")

    response = await client.post("/pvz_groups", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["owner_id"] == TEST_OWNER_ID
    assert "id" in data


@pytest.mark.asyncio
async def test_get_group_by_id(client, session):
    """
    Тест: Получение группы по ID.
    GET /pvz_groups/{group_id}
    """
    group = await GroupFactory.create_async(session, owner_id=TEST_OWNER_ID)

    response = await client.get(f"/pvz_groups/{group.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == group.id


@pytest.mark.asyncio
async def test_get_groups_by_owner_and_responsible(client, session):
    """
    Сценарий:
    owner создает 3 группы:
    - 2 с responsible_id
    - 1 без responsible_id
    Проверяем, что при фильтрации по responsible_id
    возвращаются только нужные группы owner'а
    """

    owner = await EmployeeFactory.create_async(session, user_id=TEST_OWNER_ID)
    responsible = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)

    group_1 = await GroupFactory.create_async(
        session,
        owner_id=owner.user_id,
        responsible_id=responsible.user_id,
    )
    group_2 = await GroupFactory.create_async(
        session,
        owner_id=owner.user_id,
        responsible_id=responsible.user_id,
    )
    await GroupFactory.create_async(
        session,
        owner_id=owner.user_id,
        responsible_id=None,
    )

    response = await client.get(
        "/pvz_groups",
        params={"responsible_id": responsible.user_id},
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    received_ids = {group["id"] for group in data}
    expected_ids = {group_1.id, group_2.id}

    assert received_ids == expected_ids


@pytest.mark.asyncio
async def test_update_group(client, session):
    """
    Тест: Обновление данных группы.
    PATCH /pvz_groups/{group_id}
    """
    group = await GroupFactory.create_async(session, owner_id=TEST_OWNER_ID)
    new_responsible = await EmployeeFactory.create_async(session)

    update_payload = {"responsible_id": new_responsible.user_id, "name": "Updated Name Group"}

    response = await client.patch(f"/pvz_groups/{group.id}", json=update_payload)

    assert response.status_code == 200

    data = response.json()
    assert data["responsible_id"] == new_responsible.user_id
    assert data["name"] == "Updated Name Group"


@pytest.mark.asyncio
async def test_assign_responsible_to_group_cascade(client, session):
    """
    Тест: Назначение куратора группе.
    PATCH /pvz_groups/{group_id}/responsible
    Проверяет, что куратор проставился У ГРУППЫ и У ВСЕХ ЕЁ ПВЗ.
    """
    responsible = await EmployeeFactory.create_async(session, owner_id=TEST_OWNER_ID)
    group = await GroupFactory.create_async(session, owner_id=TEST_OWNER_ID)

    for _ in range(3):
        await PVZFactory.create_async(session, group_id=group.id)

    other_pvz = await PVZFactory.create_async(session, responsible_id=None)

    response = await client.patch(f"/pvz_groups/{group.id}/responsible", params={"responsible_id": responsible.user_id})

    assert response.status_code == 200

    await session.refresh(group)
    assert group.responsible_id == responsible.user_id

    stmt = select(PVZs).where(PVZs.group_id == group.id)
    result = await session.execute(stmt)
    updated_pvzs = result.scalars().all()

    for pvz in updated_pvzs:
        assert pvz.responsible_id == responsible.user_id

    await session.refresh(other_pvz)
    assert other_pvz.responsible_id is None


@pytest.mark.asyncio
async def test_delete_group_and_unassign_pvzs(client, session):
    """
    Тест: Удаление группы.
    DELETE /pvz_groups/{group_id}
    Проверяет:
    1. Группа удалена из БД.
    2. ПВЗ, которые были в группе, отвязались (group_id -> None).
    """
    group = await GroupFactory.create_async(session, owner_id=TEST_OWNER_ID)
    pvz = await PVZFactory.create_async(session, group_id=group.id, owner_id=TEST_OWNER_ID)

    group_id = group.id

    response = await client.delete(f"/pvz_groups/{group_id}")

    assert response.status_code == 204

    deleted_group = await session.get(PVZGroups, group_id)
    assert deleted_group is None

    await session.refresh(pvz)

    assert pvz.group_id is None
