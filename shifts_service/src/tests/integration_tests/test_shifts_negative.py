from datetime import datetime, timedelta

import pytest

from src.tests.factories import ShiftFactory


class TestShiftNotFound:
    """Негативные тесты для несуществующих смен (404)"""

    @pytest.mark.parametrize(
        "non_existent_id",
        [
            pytest.param(999999, id="large_id"),
            pytest.param(1, id="small_id"),
            pytest.param(123456, id="random_id"),
        ],
    )
    async def test_get_shift_not_found(self, client, session, non_existent_id):
        """
        Тест: Получение несуществующей смены (404).
        GET /shifts/{shift_id}
        Проверяет корректную ошибку при отсутствии записи.
        """
        response = await client.get(f"/shifts/{non_existent_id}")

        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "not_found"

    @pytest.mark.parametrize(
        "non_existent_id,update_data",
        [
            pytest.param(
                999999,
                {"scheduled_shift_id": 1},
                id="update_large_id",
            ),
            pytest.param(
                1,
                {"ended_at": datetime.now().isoformat()},
                id="update_small_id",
            ),
            pytest.param(
                55555,
                {"scheduled_shift_id": 50, "ended_at": datetime.now().isoformat()},
                id="update_random_id_multiple_fields",
            ),
        ],
    )
    async def test_update_shift_not_found(self, client, session, non_existent_id, update_data):
        """
        Тест: Обновление несуществующей смены (404).
        PATCH /shifts/{shift_id}
        """
        response = await client.patch(f"/shifts/{non_existent_id}", json=update_data)

        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "not_found"

    @pytest.mark.parametrize(
        "non_existent_id",
        [
            pytest.param(999999, id="delete_large_id"),
            pytest.param(1, id="delete_small_id"),
            pytest.param(777777, id="delete_random_id"),
        ],
    )
    async def test_delete_shift_not_found(self, client, session, non_existent_id):
        """
        Тест: Удаление несуществующей смены (404).
        DELETE /shifts/{shift_id}
        """
        response = await client.delete(f"/shifts/{non_existent_id}")

        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "not_found"


class TestValidationErrors:
    """Негативные тесты для ошибок валидации (422)"""

    @pytest.mark.parametrize(
        "payload,expected_error_contains",
        [
            pytest.param(
                {},
                "scheduled_shift_id",
                id="missing_required_field",
            ),
            pytest.param(
                {"scheduled_shift_id": "not_a_number"},
                "int",
                id="invalid_type_string_for_int",
            ),
            pytest.param(
                {"scheduled_shift_id": None},
                "none is not an allowed value",
                id="null_required_field",
            ),
            pytest.param(
                {"scheduled_shift_id": 1, "started_at": "invalid_date"},
                "datetime",
                id="invalid_datetime_format",
            ),
        ],
    )
    async def test_create_shift_validation_error(self, client, session, payload, expected_error_contains):
        """
        Тест: Ошибка валидации при создании смены (422).
        POST /shifts
        Проверяет обработку некорректных данных.
        """
        response = await client.post("/shifts", json=payload)

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "started_at_offset,ended_at_offset,should_fail",
        [
            pytest.param(0, -1, True, id="ended_before_started"),
            pytest.param(0, 0, True, id="ended_equals_started"),
            pytest.param(0, 1, False, id="ended_after_started_valid"),
        ],
    )
    async def test_create_shift_ended_at_validation(
        self, client, session, started_at_offset, ended_at_offset, should_fail
    ):
        """
        Тест: Валидация ended_at относительно started_at.
        POST /shifts
        Проверяет, что ended_at должен быть больше started_at.
        """
        now = datetime.now()
        started_at = now + timedelta(hours=started_at_offset)
        ended_at = now + timedelta(hours=ended_at_offset)

        payload = {
            "scheduled_shift_id": 1,
            "started_at": started_at.isoformat(),
            "ended_at": ended_at.isoformat(),
        }

        response = await client.post("/shifts", json=payload)

        if should_fail:
            assert response.status_code == 422
        else:
            assert response.status_code == 201


class TestInvalidPathParameters:
    """Тесты для некорректных параметров пути"""

    @pytest.mark.parametrize(
        "invalid_id",
        [
            pytest.param("abc", id="string_id"),
            pytest.param("1.5", id="float_id"),
            pytest.param("null", id="null_string_id"),
        ],
    )
    async def test_get_shift_invalid_id_format(self, client, session, invalid_id):
        """
        Тест: Получение смены с некорректным форматом ID (422).
        GET /shifts/{shift_id}
        """
        response = await client.get(f"/shifts/{invalid_id}")

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "invalid_id",
        [
            pytest.param("abc", id="string_id"),
            pytest.param("test", id="word_id"),
        ],
    )
    async def test_update_shift_invalid_id_format(self, client, session, invalid_id):
        """
        Тест: Обновление смены с некорректным форматом ID (422).
        PATCH /shifts/{shift_id}
        """
        response = await client.patch(f"/shifts/{invalid_id}", json={"scheduled_shift_id": 1})

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "invalid_id",
        [
            pytest.param("abc", id="string_id"),
            pytest.param("delete_me", id="word_id"),
        ],
    )
    async def test_delete_shift_invalid_id_format(self, client, session, invalid_id):
        """
        Тест: Удаление смены с некорректным форматом ID (422).
        DELETE /shifts/{shift_id}
        """
        response = await client.delete(f"/shifts/{invalid_id}")

        assert response.status_code == 422


class TestInvalidQueryParameters:
    """Тесты для некорректных query-параметров"""

    @pytest.mark.parametrize(
        "params,expected_status",
        [
            pytest.param(
                {"page": 0},
                422,
                id="zero_page",
            ),
            pytest.param(
                {"size": 0},
                422,
                id="zero_size",
            ),
            pytest.param(
                {"page": -1},
                422,
                id="negative_page",
            ),
            pytest.param(
                {"size": -1},
                422,
                id="negative_size",
            ),
            pytest.param(
                {"scheduled_shift_id": "not_a_number"},
                422,
                id="invalid_scheduled_shift_id",
            ),
            pytest.param(
                {"is_active": "maybe"},
                422,
                id="invalid_boolean",
            ),
        ],
    )
    async def test_get_shifts_invalid_params(self, client, session, params, expected_status):
        """
        Тест: Некорректные query-параметры при получении списка смен (422).
        GET /shifts
        """
        response = await client.get("/shifts", params=params)

        assert response.status_code == expected_status


class TestUpdateValidationErrors:
    """Тесты для ошибок валидации при обновлении"""

    @pytest.mark.parametrize(
        "update_payload",
        [
            pytest.param(
                {"scheduled_shift_id": "not_a_number"},
                id="invalid_scheduled_id_type",
            ),
            pytest.param(
                {"started_at": "invalid_date"},
                id="invalid_started_at_format",
            ),
            pytest.param(
                {"ended_at": "not_a_datetime"},
                id="invalid_ended_at_format",
            ),
        ],
    )
    async def test_update_shift_validation_error(self, client, session, update_payload):
        """
        Тест: Ошибка валидации при обновлении смены (422).
        PATCH /shifts/{shift_id}
        """
        shift = await ShiftFactory.create_async(session)

        response = await client.patch(f"/shifts/{shift.id}", json=update_payload)

        assert response.status_code == 422


class TestEmptyAndEdgeCases:
    """Тесты для граничных случаев"""

    async def test_get_shifts_empty_list(self, client, session):
        """
        Тест: Получение пустого списка смен.
        GET /shifts
        """
        response = await client.get("/shifts")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    @pytest.mark.parametrize(
        "page,size",
        [
            pytest.param(100, 10, id="page_beyond_total"),
            pytest.param(50, 50, id="large_page_large_size"),
        ],
    )
    async def test_get_shifts_page_beyond_total(self, client, session, page, size):
        """
        Тест: Запрос страницы, превышающей общее количество записей.
        GET /shifts
        """
        for _ in range(3):
            await ShiftFactory.create_async(session)

        response = await client.get("/shifts", params={"page": page, "size": size})

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 3

    async def test_update_with_empty_body(self, client, session):
        """
        Тест: Обновление смены с пустым телом запроса.
        PATCH /shifts/{shift_id}
        """
        shift = await ShiftFactory.create_async(session)

        response = await client.patch(f"/shifts/{shift.id}", json={})

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == shift.id

    async def test_delete_already_deleted_shift(self, client, session):
        """
        Тест: Повторное удаление уже удаленной смены (404).
        DELETE /shifts/{shift_id}
        """
        shift = await ShiftFactory.create_async(session)
        shift_id = shift.id

        response1 = await client.delete(f"/shifts/{shift_id}")
        assert response1.status_code == 204

        response2 = await client.delete(f"/shifts/{shift_id}")
        assert response2.status_code == 404
