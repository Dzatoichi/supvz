import pytest
from sqlalchemy import select

from src.models.pvzs.PVZGroups import PVZGroups
from src.models.pvzs.PVZs import PVZs
from src.tests.factories import EmployeeFactory, GroupFactory, PVZFactory

pytestmark = pytest.mark.anyio


@pytest.mark.asyncio
async def test_create_group(client, session):
    """
    Тест: Успешное создание группы ПВЗ.
    POST /pvz_groups/
    """
    owner = await EmployeeFactory.create_async(session)

    payload_model = GroupFactory.build(owner_id=owner.user_id)
    payload = payload_model.model_dump(mode="json")

    response = await client.post("/pvz_groups", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["owner_id"] == owner.user_id
    assert "id" in data


@pytest.mark.asyncio
async def test_get_group_by_id(client, session):
    """
    Тест: Получение группы по ID.
    GET /pvz_groups/{group_id}
    """
    group = await GroupFactory.create_async(session)

    response = await client.get(f"/pvz_groups/{group.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == group.id


@pytest.mark.asyncio
async def test_get_groups_filter(client, session):
    """
    Тест: Получение списка групп с фильтрацией по owner_id.
    GET /pvz_groups?owner_id=...
    """
    target_owner = await EmployeeFactory.create_async(session)
    other_owner = await EmployeeFactory.create_async(session)

    groups_target = []
    for _ in range(2):
        group = await GroupFactory.create_async(session, owner_id=target_owner.user_id)
        groups_target.append(group)

    await GroupFactory.create_async(session, owner_id=other_owner.user_id)

    response = await client.get("/pvz_groups", params={"owner_id": target_owner.user_id})

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    received_ids = {g["id"] for g in data}
    expected_ids = {g.id for g in groups_target}
    assert received_ids == expected_ids


@pytest.mark.asyncio
async def test_update_group(client, session):
    """
    Тест: Обновление данных группы.
    PATCH /pvz_groups/{group_id}
    """
    group = await GroupFactory.create_async(session)
    new_curator = await EmployeeFactory.create_async(session)

    update_payload = {"curator_id": new_curator.user_id, "name": "Updated Name Group"}

    response = await client.patch(f"/pvz_groups/{group.id}", json=update_payload)
    if response.status_code != 200:
        print(f"\nERROR BODY: {response.json()}\n")
    assert response.status_code == 200

    data = response.json()
    assert data["curator_id"] == new_curator.user_id
    assert data["name"] == "Updated Name Group"


@pytest.mark.asyncio
async def test_assign_curator_to_group_cascade(client, session):
    """
    Тест: Назначение куратора группе.
    PATCH /pvz_groups/{group_id}/curator
    Проверяет, что куратор проставился У ГРУППЫ и У ВСЕХ ЕЁ ПВЗ.
    """
    curator = await EmployeeFactory.create_async(session)
    group = await GroupFactory.create_async(session)

    for _ in range(3):
        await PVZFactory.create_async(session, group_id=group.id)

    other_pvz = await PVZFactory.create_async(session, curator_id=None)

    response = await client.patch(f"/pvz_groups/{group.id}/curator", params={"curator_id": curator.user_id})

    assert response.status_code == 200

    await session.refresh(group)
    assert group.curator_id == curator.user_id

    stmt = select(PVZs).where(PVZs.group_id == group.id)
    result = await session.execute(stmt)
    updated_pvzs = result.scalars().all()

    for pvz in updated_pvzs:
        assert pvz.curator_id == curator.user_id

    await session.refresh(other_pvz)
    assert other_pvz.curator_id is None


@pytest.mark.asyncio
async def test_delete_group_and_unassign_pvzs(client, session):
    """
    Тест: Удаление группы.
    DELETE /pvz_groups/{group_id}
    Проверяет:
    1. Группа удалена из БД.
    2. ПВЗ, которые были в группе, отвязались (group_id -> None).
    """
    group = await GroupFactory.create_async(session)
    pvz = await PVZFactory.create_async(session, group_id=group.id)

    group_id = group.id

    response = await client.delete(f"/pvz_groups/{group_id}")

    assert response.status_code == 204

    deleted_group = await session.get(PVZGroups, group_id)
    assert deleted_group is None

    await session.refresh(pvz)

    assert pvz.group_id is None
