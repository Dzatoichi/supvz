from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi_pagination import Page

from src.main import app
from src.schemas.scheduled_shifts_schemas import ScheduledShiftReadSchema
from src.services.scheduled_shifts_service import ScheduledShiftsService
from src.utils.dependencies import get_scheduled_shifts_dao, get_scheduled_shifts_service

pytestmark = pytest.mark.anyio


@pytest.fixture(autouse=True)
def override_dependencies():
    """Фикстура для переопределения зависимостей."""
    # Создаем мок-сервис
    mock_service = AsyncMock(spec=ScheduledShiftsService)

    # Создаем тестовую смену
    test_shift = ScheduledShiftReadSchema(
        id=1,
        pvz_id=1,
        user_id=1,
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, hours=8),
        completed=False,
        status="scheduled",
        paid=False,
    )

    # Настраиваем моки
    mock_service.create_scheduled_shift.return_value = test_shift
    mock_service.get_scheduled_shift_by_id.return_value = test_shift
    mock_service.update_scheduled_shift.return_value = test_shift
    mock_service.delete_scheduled_shift.return_value = None

    # Создаем правильный объект Page для get_scheduled_shifts
    mock_page = Page(items=[test_shift], total=1, page=1, size=10, pages=1)
    mock_service.get_scheduled_shifts.return_value = mock_page

    # Мок репозитория
    mock_repo = AsyncMock()

    # Переопределяем зависимости
    app.dependency_overrides[get_scheduled_shifts_service] = lambda: mock_service
    app.dependency_overrides[get_scheduled_shifts_dao] = lambda: mock_repo

    yield

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


# Тесты, которые используют стандартную фикстуру
async def test_create_scheduled_shift_success(client):
    """Тест: POST /scheduled_shifts/ должен успешно создать запланированную смену."""
    shift_data = {
        "pvz_id": 1,
        "user_id": 1,
        "starts_at": (datetime.now() + timedelta(days=1)).isoformat(),
        "ends_at": (datetime.now() + timedelta(days=1, hours=8)).isoformat(),
    }

    response = client.post("/scheduled_shifts/", json=shift_data)

    assert response.status_code == 200
    data = response.json()
    assert data["pvz_id"] == 1
    assert data["user_id"] == 1
    assert data["status"] == "scheduled"
    assert data["completed"] is False
    assert data["paid"] is False


async def test_get_scheduled_shifts_with_filters(client):
    """
    Тест: GET /scheduled_shifts/ с фильтрами должен вернуть отфильтрованный список.
    """
    response = client.get(
        "/scheduled_shifts/", params={"user_id": 1, "completed": False, "status": "scheduled", "size": 10, "page": 1}
    )

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


async def test_get_scheduled_shift_by_id_success(client):
    """Тест: GET /scheduled_shifts/{id} должен вернуть смену по ID."""
    response = client.get("/scheduled_shifts/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "starts_at" in data
    assert "ends_at" in data


async def test_delete_scheduled_shift_success(client):
    """Тест: DELETE /scheduled_shifts/{id} должен успешно удалить смену."""
    response = client.delete("/scheduled_shifts/1")

    assert response.status_code == 200


async def test_create_shift_with_invalid_dates(client):
    """Тест: POST /scheduled_shifts/ должен вернуть 422 при некорректных датах."""
    shift_data = {
        "pvz_id": 1,
        "user_id": 1,
        "starts_at": (datetime.now() + timedelta(days=2)).isoformat(),
        "ends_at": (datetime.now() + timedelta(days=1)).isoformat(),  # ends_at раньше starts_at
    }

    response = client.post("/scheduled_shifts/", json=shift_data)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


# Тесты, которым нужны специальные моки
async def test_get_scheduled_shifts_with_filters_empty_result():
    """
    Тест: GET /scheduled_shifts/ должен вернуть пустой список при отсутствии результатов.
    """
    # Создаем новый мок сервиса для этого теста
    mock_service = AsyncMock(spec=ScheduledShiftsService)

    # Создаем пустой Page
    empty_page = Page(items=[], total=0, page=1, size=10, pages=0)
    mock_service.get_scheduled_shifts.return_value = empty_page

    # Мок репозитория
    mock_repo = AsyncMock()

    # Переопределяем зависимости для этого теста
    app.dependency_overrides[get_scheduled_shifts_service] = lambda: mock_service
    app.dependency_overrides[get_scheduled_shifts_dao] = lambda: mock_repo

    try:
        client = TestClient(app)
        response = client.get("/scheduled_shifts/", params={"user_id": 999, "size": 10, "page": 1})

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
    finally:
        # Восстанавливаем оригинальные зависимости
        app.dependency_overrides.clear()


async def test_update_scheduled_shift_success():
    """
    Тест: PATCH /scheduled_shifts/{id} должен успешно обновить смену.
    """
    # Создаем обновленную смену
    updated_shift = ScheduledShiftReadSchema(
        id=1,
        pvz_id=1,
        user_id=1,
        starts_at=datetime.now(),
        ends_at=datetime.now() + timedelta(hours=8),
        completed=True,
        status="completed",
        paid=True,
    )

    # Создаем новый мок сервиса для этого теста
    mock_service = AsyncMock(spec=ScheduledShiftsService)
    mock_service.update_scheduled_shift.return_value = updated_shift

    # Мок репозитория
    mock_repo = AsyncMock()

    # Временно переопределяем зависимость
    app.dependency_overrides[get_scheduled_shifts_service] = lambda: mock_service
    app.dependency_overrides[get_scheduled_shifts_dao] = lambda: mock_repo

    try:
        client = TestClient(app)
        update_data = {
            "completed": True,
            "status": "completed",
            "paid": True,
        }

        response = client.patch("/scheduled_shifts/1", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["status"] == "completed"
        assert data["paid"] is True
    finally:
        # Восстанавливаем оригинальные зависимости
        app.dependency_overrides.clear()


async def test_update_scheduled_shift_partial_success():
    """
    Тест: PATCH /scheduled_shifts/{id} должен успешно обновить смену частично.
    """
    # Создаем обновленную смену с частичными изменениями
    updated_shift = ScheduledShiftReadSchema(
        id=1,
        pvz_id=1,
        user_id=1,
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, hours=8),
        completed=True,  # Только это поле изменили
        status="scheduled",
        paid=False,
    )

    # Создаем новый мок сервиса
    mock_service = AsyncMock(spec=ScheduledShiftsService)
    mock_service.update_scheduled_shift.return_value = updated_shift

    # Мок репозитория
    mock_repo = AsyncMock()

    # Временно переопределяем зависимость
    app.dependency_overrides[get_scheduled_shifts_service] = lambda: mock_service
    app.dependency_overrides[get_scheduled_shifts_dao] = lambda: mock_repo

    try:
        client = TestClient(app)
        update_data = {
            "completed": True,  # Только одно поле
        }

        response = client.patch("/scheduled_shifts/1", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["status"] == "scheduled"  # Осталось прежним
        assert data["paid"] is False  # Осталось прежним
    finally:
        # Восстанавливаем оригинальные зависимости
        app.dependency_overrides.clear()


async def test_get_scheduled_shift_by_id_not_found():
    """Тест: GET /scheduled_shifts/{id} должен вернуть 404, если смена не найдена."""
    # Создаем новый мок сервиса
    mock_service = AsyncMock(spec=ScheduledShiftsService)
    mock_service.get_scheduled_shift_by_id.side_effect = HTTPException(
        status_code=404, detail="Scheduled shift not found"
    )

    # Мок репозитория
    mock_repo = AsyncMock()

    # Временно переопределяем зависимость
    app.dependency_overrides[get_scheduled_shifts_service] = lambda: mock_service
    app.dependency_overrides[get_scheduled_shifts_dao] = lambda: mock_repo

    try:
        client = TestClient(app)
        response = client.get("/scheduled_shifts/999")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Scheduled shift not found"
    finally:
        # Восстанавливаем оригинальные зависимости
        app.dependency_overrides.clear()


async def test_delete_scheduled_shift_not_found():
    """Тест: DELETE /scheduled_shifts/{id} должен вернуть 404, если смена не найдена."""
    # Создаем новый мок сервиса
    mock_service = AsyncMock(spec=ScheduledShiftsService)
    mock_service.delete_scheduled_shift.side_effect = HTTPException(status_code=404, detail="Scheduled shift not found")

    # Мок репозитория
    mock_repo = AsyncMock()

    # Временно переопределяем зависимость
    app.dependency_overrides[get_scheduled_shifts_service] = lambda: mock_service
    app.dependency_overrides[get_scheduled_shifts_dao] = lambda: mock_repo

    try:
        client = TestClient(app)
        response = client.delete("/scheduled_shifts/999")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Scheduled shift not found"
    finally:
        # Восстанавливаем оригинальные зависимости
        app.dependency_overrides.clear()


# Дополнительные тесты для проверки валидации схемы
async def test_create_shift_with_missing_required_fields(client):
    """Тест: POST /scheduled_shifts/ должен вернуть 422 при отсутствии обязательных полей."""
    shift_data = {
        "pvz_id": 1,
        # Отсутствует user_id
        "starts_at": datetime.now().isoformat(),
    }

    response = client.post("/scheduled_shifts/", json=shift_data)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


async def test_get_scheduled_shifts_404_on_empty_filtered_results():
    """
    Тест: GET /scheduled_shifts/ должен вернуть 404, если смены не найдены.
    """
    # Создаем новый мок сервиса
    mock_service = AsyncMock(spec=ScheduledShiftsService)
    mock_service.get_scheduled_shifts.side_effect = HTTPException(status_code=404, detail="Смены не найдены")

    # Мок репозитория
    mock_repo = AsyncMock()

    # Временно переопределяем зависимость
    app.dependency_overrides[get_scheduled_shifts_service] = lambda: mock_service
    app.dependency_overrides[get_scheduled_shifts_dao] = lambda: mock_repo

    try:
        client = TestClient(app)
        response = client.get("/scheduled_shifts/", params={"user_id": 999})
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Смены не найдены"
    finally:
        # Восстанавливаем оригинальные зависимости
        app.dependency_overrides.clear()
