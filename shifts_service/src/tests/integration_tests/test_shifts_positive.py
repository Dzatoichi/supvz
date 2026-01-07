from datetime import datetime, timedelta

import pytest

from src.tests.factories import ShiftFactory


class TestCreateShift:
    """Тесты для создания смен (POST /shifts)"""

    @pytest.mark.parametrize(
        "shift_data",
        [
            pytest.param(
                {"scheduled_shift_id": 1},
                id="minimal_data",
            ),
            pytest.param(
                {
                    "scheduled_shift_id": 42,
                    "started_at": datetime.now().isoformat(),
                },
                id="with_started_at",
            ),
            pytest.param(
                {
                    "scheduled_shift_id": 100,
                    "started_at": datetime.now().isoformat(),
                    "ended_at": (datetime.now() + timedelta(hours=8)).isoformat(),
                },
                id="full_data_with_ended_at",
            ),
        ],
    )
    async def test_create_shift_success(self, client, session, shift_data):
        """
        Тест: Успешное создание смены с различными наборами данных.
        POST /shifts
        Проверяет создание смены с минимальными и полными данными.
        """
        response = await client.post("/shifts", json=shift_data)

        assert response.status_code == 201
        data = response.json()
        assert data["scheduled_shift_id"] == shift_data["scheduled_shift_id"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.parametrize(
        "scheduled_shift_id",
        [
            pytest.param(1, id="scheduled_id_1"),
            pytest.param(50, id="scheduled_id_50"),
            pytest.param(999, id="scheduled_id_999"),
        ],
    )
    async def test_create_shift_various_scheduled_ids(self, client, session, scheduled_shift_id):
        """
        Тест: Создание смены с различными scheduled_shift_id.
        POST /shifts
        """
        shift_data = {"scheduled_shift_id": scheduled_shift_id}

        response = await client.post("/shifts", json=shift_data)

        assert response.status_code == 201
        data = response.json()
        assert data["scheduled_shift_id"] == scheduled_shift_id


class TestGetShift:
    """Тесты для получения смен (GET /shifts/{shift_id} и GET /shifts)"""

    async def test_get_shift_by_id_success(self, client, session):
        """
        Тест: Получение смены по ID.
        GET /shifts/{shift_id}
        Проверяет соответствие возвращаемых данных созданным в БД.
        """
        shift = await ShiftFactory.create_async(session)

        response = await client.get(f"/shifts/{shift.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == shift.id
        assert data["scheduled_shift_id"] == shift.scheduled_shift_id

    @pytest.mark.parametrize(
        "shifts_count",
        [
            pytest.param(0, id="empty_list"),
            pytest.param(1, id="single_shift"),
            pytest.param(5, id="multiple_shifts"),
            pytest.param(15, id="many_shifts_with_pagination"),
        ],
    )
    async def test_get_shifts_list(self, client, session, shifts_count):
        """
        Тест: Получение списка смен с различным количеством записей.
        GET /shifts
        Проверяет корректность пагинации и total count.
        """
        for _ in range(shifts_count):
            await ShiftFactory.create_async(session)

        response = await client.get("/shifts")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == shifts_count

    @pytest.mark.parametrize(
        "page,size,expected_items",
        [
            pytest.param(1, 5, 5, id="first_page_5_items"),
            pytest.param(2, 5, 5, id="second_page_5_items"),
            pytest.param(1, 10, 10, id="first_page_10_items"),
            pytest.param(3, 5, 2, id="third_page_2_items"),
        ],
    )
    async def test_get_shifts_pagination(self, client, session, page, size, expected_items):
        """
        Тест: Проверка пагинации списка смен.
        GET /shifts?page={page}&size={size}
        """
        for i in range(12):
            await ShiftFactory.create_async(session, scheduled_shift_id=i + 1)

        response = await client.get("/shifts", params={"page": page, "size": size})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == expected_items
        assert data["total"] == 12


class TestFilterShifts:
    """Тесты для фильтрации смен"""

    @pytest.mark.parametrize(
        "target_scheduled_id,total_shifts,expected_filtered",
        [
            pytest.param(10, 5, 3, id="filter_3_of_5"),
            pytest.param(20, 10, 5, id="filter_5_of_10"),
            pytest.param(30, 7, 1, id="filter_1_of_7"),
        ],
    )
    async def test_filter_by_scheduled_shift_id(
        self, client, session, target_scheduled_id, total_shifts, expected_filtered
    ):
        """
        Тест: Фильтрация смен по scheduled_shift_id.
        GET /shifts?scheduled_shift_id={id}
        """
        for _ in range(expected_filtered):
            await ShiftFactory.create_async(session, scheduled_shift_id=target_scheduled_id)

        for i in range(total_shifts - expected_filtered):
            await ShiftFactory.create_async(session, scheduled_shift_id=target_scheduled_id + i + 1)

        response = await client.get("/shifts", params={"scheduled_shift_id": target_scheduled_id})

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == expected_filtered
        for item in data["items"]:
            assert item["scheduled_shift_id"] == target_scheduled_id

    @pytest.mark.parametrize(
        "is_active,create_ended,expected_count",
        [
            pytest.param(True, False, 3, id="only_active_shifts"),
            pytest.param(False, True, 2, id="only_inactive_shifts"),
        ],
    )
    async def test_filter_by_is_active(self, client, session, is_active, create_ended, expected_count):
        """
        Тест: Фильтрация смен по активности (is_active).
        GET /shifts?is_active={bool}
        """
        now = datetime.now()

        for _ in range(3):
            await ShiftFactory.create_async(
                session,
                started_at=now,
                ended_at=None,
            )

        for _ in range(2):
            await ShiftFactory.create_async(
                session,
                started_at=now - timedelta(hours=8),
                ended_at=now,
            )

        response = await client.get("/shifts", params={"is_active": is_active})

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == expected_count


class TestUpdateShift:
    """Тесты для обновления смен (PATCH /shifts/{shift_id})"""

    @pytest.mark.parametrize(
        "update_data,expected_field",
        [
            pytest.param(
                {"scheduled_shift_id": 999},
                "scheduled_shift_id",
                id="update_scheduled_id",
            ),
            pytest.param(
                {"ended_at": (datetime.now() + timedelta(hours=8)).isoformat()},
                "ended_at",
                id="update_ended_at",
            ),
        ],
    )
    async def test_update_shift_success(self, client, session, update_data, expected_field):
        """
        Тест: Успешное обновление смены.
        PATCH /shifts/{shift_id}
        Проверяет обновление различных полей.
        """
        shift = await ShiftFactory.create_async(session)

        response = await client.patch(f"/shifts/{shift.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == shift.id

        if expected_field in update_data:
            if expected_field == "scheduled_shift_id":
                assert data[expected_field] == update_data[expected_field]
            elif expected_field == "ended_at":
                assert data[expected_field] is not None

    async def test_update_shift_multiple_fields(self, client, session):
        """
        Тест: Обновление нескольких полей смены одновременно.
        PATCH /shifts/{shift_id}
        """
        shift = await ShiftFactory.create_async(session)
        new_scheduled_id = 777
        new_ended_at = (datetime.now() + timedelta(hours=10)).isoformat()

        update_data = {
            "scheduled_shift_id": new_scheduled_id,
            "ended_at": new_ended_at,
        }

        response = await client.patch(f"/shifts/{shift.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["scheduled_shift_id"] == new_scheduled_id
        assert data["ended_at"] is not None


class TestDeleteShift:
    """Тесты для удаления смен (DELETE /shifts/{shift_id})"""

    async def test_delete_shift_success(self, client, session):
        """
        Тест: Успешное удаление смены.
        DELETE /shifts/{shift_id}
        Проверяет статус ответа и отсутствие записи после удаления.
        """
        shift = await ShiftFactory.create_async(session)

        response = await client.delete(f"/shifts/{shift.id}")

        assert response.status_code == 204

        get_response = await client.get(f"/shifts/{shift.id}")
        assert get_response.status_code == 404

    @pytest.mark.parametrize(
        "shifts_to_create,shift_to_delete_index",
        [
            pytest.param(3, 0, id="delete_first"),
            pytest.param(3, 1, id="delete_middle"),
            pytest.param(3, 2, id="delete_last"),
        ],
    )
    async def test_delete_specific_shift(self, client, session, shifts_to_create, shift_to_delete_index):
        """
        Тест: Удаление конкретной смены из списка.
        DELETE /shifts/{shift_id}
        Проверяет, что удаляется только указанная смена.
        """
        shifts = []
        for i in range(shifts_to_create):
            shift = await ShiftFactory.create_async(session, scheduled_shift_id=i + 100)
            shifts.append(shift)

        shift_to_delete = shifts[shift_to_delete_index]

        response = await client.delete(f"/shifts/{shift_to_delete.id}")
        assert response.status_code == 204

        # Проверяем, что остальные смены на месте
        list_response = await client.get("/shifts")
        data = list_response.json()
        assert data["total"] == shifts_to_create - 1

        remaining_ids = [item["id"] for item in data["items"]]
        assert shift_to_delete.id not in remaining_ids
