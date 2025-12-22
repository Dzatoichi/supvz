from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from fastapi_pagination import Page, Params

from src.schemas.scheduled_shifts_schemas import (
    ScheduledShiftCreateSchema,
    ScheduledShiftReadSchema,
    ScheduledShiftUpdateSchema,
)
from src.services.scheduled_shifts_service import ScheduledShiftsService

pytestmark = pytest.mark.asyncio


class TestScheduledShiftsService:
    async def test_create_scheduled_shift_success(self):
        """
        Тест на успешное создание запланированной смены.
        """
        mock_repo = AsyncMock()

        mock_created_shift = MagicMock()
        mock_created_shift.id = 1
        mock_created_shift.pvz_id = 1
        mock_created_shift.user_id = 1
        mock_created_shift.starts_at = datetime.now() + timedelta(days=1)
        mock_created_shift.ends_at = datetime.now() + timedelta(days=1, hours=8)
        mock_created_shift.completed = False
        mock_created_shift.status = "scheduled"
        mock_created_shift.paid = False
        mock_created_shift.created_at = datetime.now()
        mock_created_shift.updated_at = datetime.now()

        mock_repo.create.return_value = mock_created_shift

        shift_data = ScheduledShiftCreateSchema(
            pvz_id=1,
            user_id=1,
            starts_at=datetime.now() + timedelta(days=1),
            ends_at=datetime.now() + timedelta(days=1, hours=8),
        )

        service = ScheduledShiftsService()
        result = await service.create_scheduled_shift(shift_data, mock_repo)

        assert isinstance(result, ScheduledShiftReadSchema)
        assert result.id == 1
        assert result.pvz_id == 1
        assert result.completed is False

        mock_repo.create.assert_called_once()

    async def test_get_scheduled_shift_by_id_success(self):
        """
        Тест на успешное получение смены по ID.
        """
        mock_repo = AsyncMock()

        mock_shift = MagicMock()
        mock_shift.id = 1
        mock_shift.pvz_id = 1
        mock_shift.user_id = 1
        mock_shift.starts_at = datetime.now()
        mock_shift.ends_at = datetime.now() + timedelta(hours=8)
        mock_shift.completed = False
        mock_shift.status = "scheduled"
        mock_shift.paid = False
        mock_shift.created_at = datetime.now()
        mock_shift.updated_at = datetime.now()

        mock_repo.get_by_id.return_value = mock_shift

        service = ScheduledShiftsService()
        result = await service.get_scheduled_shift_by_id(1, mock_repo)

        assert isinstance(result, ScheduledShiftReadSchema)
        assert result.id == 1
        mock_repo.get_by_id.assert_called_once_with(1)

    async def test_get_scheduled_shift_by_id_not_found(self):
        """
        Тест на 404 при получении несуществующей смены.
        """
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None

        service = ScheduledShiftsService()

        with pytest.raises(HTTPException) as exc_info:
            await service.get_scheduled_shift_by_id(999, mock_repo)

        assert exc_info.value.status_code == 404
        assert "Смена не найдена" in str(exc_info.value.detail)

    async def test_get_scheduled_shifts_with_filters_success(self):
        """
        Тест на успешное получение смен с фильтрами.
        """
        mock_repo = AsyncMock()

        # Мок пагинированного результата
        mock_paginated = MagicMock(spec=Page)

        mock_shift = MagicMock()
        mock_shift.id = 1
        mock_shift.pvz_id = 1
        mock_shift.user_id = 1
        mock_shift.starts_at = datetime.now()
        mock_shift.ends_at = datetime.now() + timedelta(hours=8)
        mock_shift.completed = False
        mock_shift.status = "scheduled"
        mock_shift.paid = False
        mock_shift.created_at = datetime.now()
        mock_shift.updated_at = datetime.now()

        mock_paginated.items = [mock_shift]
        mock_paginated.total = 1
        mock_paginated.page = 1
        mock_paginated.size = 10
        mock_paginated.pages = 1

        mock_repo.get_scheduled_shifts_filtered.return_value = mock_paginated

        service = ScheduledShiftsService()
        result = await service.get_scheduled_shifts(
            user_id=1,
            pvz_id=None,
            starts_at=None,
            ends_at=None,
            completed=False,
            status="scheduled",
            paid=None,
            repo=mock_repo,
            params=Params(page=1, size=10),
        )

        assert len(result.items) == 1
        assert isinstance(result.items[0], ScheduledShiftReadSchema)

        mock_repo.get_scheduled_shifts_filtered.assert_called_once_with(
            user_id=1,
            pvz_id=None,
            starts_at=None,
            ends_at=None,
            completed=False,
            status="scheduled",
            paid=None,
            params=Params(page=1, size=10),
        )

    async def test_get_scheduled_shifts_empty(self):
        """
        Тест на получение пустого списка смен - должен возвращать 200 с пустым списком.
        """
        mock_repo = AsyncMock()

        mock_paginated = MagicMock(spec=Page)
        mock_paginated.items = []
        mock_paginated.total = 0
        mock_paginated.page = 1
        mock_paginated.size = 10
        mock_paginated.pages = 0
        mock_repo.get_scheduled_shifts_filtered.return_value = mock_paginated

        service = ScheduledShiftsService()
        result = await service.get_scheduled_shifts(
            user_id=999,
            pvz_id=None,
            starts_at=None,
            ends_at=None,
            completed=None,
            status=None,
            paid=None,
            repo=mock_repo,
            params=Params(page=1, size=10),
        )

        assert isinstance(result, Page)
        assert len(result.items) == 0
        assert result.total == 0
        assert result.page == 1
        assert result.size == 10
        assert result.pages == 0

        mock_repo.get_scheduled_shifts_filtered.assert_called_once_with(
            user_id=999,
            pvz_id=None,
            starts_at=None,
            ends_at=None,
            completed=None,
            status=None,
            paid=None,
            params=Params(page=1, size=10),
        )

    async def test_update_scheduled_shift_success(self):
        """
        Тест на успешное обновление смены.
        """
        mock_repo = AsyncMock()

        mock_existing_shift = MagicMock()
        mock_existing_shift.id = 1
        mock_existing_shift.pvz_id = 1
        mock_existing_shift.user_id = 1
        mock_existing_shift.starts_at = datetime.now()
        mock_existing_shift.ends_at = datetime.now() + timedelta(hours=8)
        mock_existing_shift.completed = False
        mock_existing_shift.status = "scheduled"
        mock_existing_shift.paid = False
        mock_repo.get_by_id.return_value = mock_existing_shift

        mock_updated_shift = MagicMock()
        mock_updated_shift.id = 1
        mock_updated_shift.pvz_id = 1
        mock_updated_shift.user_id = 1
        mock_updated_shift.starts_at = datetime.now()
        mock_updated_shift.ends_at = datetime.now() + timedelta(hours=8)
        mock_updated_shift.completed = True
        mock_updated_shift.status = "completed"
        mock_updated_shift.paid = True
        mock_updated_shift.created_at = datetime.now()
        mock_updated_shift.updated_at = datetime.now()

        mock_repo.update.return_value = mock_updated_shift

        update_data = ScheduledShiftUpdateSchema(
            pvz_id=1,
            user_id=1,
            starts_at=datetime.now(),
            ends_at=datetime.now() + timedelta(hours=8),
            completed=True,
            status="completed",
            paid=True,
        )

        service = ScheduledShiftsService()
        result = await service.update_scheduled_shift(1, update_data, mock_repo)

        assert isinstance(result, ScheduledShiftReadSchema)
        assert result.completed is True
        assert result.status == "completed"

        mock_repo.update.assert_called_once_with(
            id=1,
            pvz_id=1,
            user_id=1,
            starts_at=update_data.starts_at,
            ends_at=update_data.ends_at,
            completed=True,
            status="completed",
            paid=True,
        )

    async def test_update_scheduled_shift_partial(self):
        """
        Тест на частичное обновление смены.
        """
        mock_repo = AsyncMock()

        mock_existing_shift = MagicMock()
        mock_existing_shift.id = 1
        mock_existing_shift.pvz_id = 1
        mock_existing_shift.user_id = 1
        mock_existing_shift.starts_at = datetime.now()
        mock_existing_shift.ends_at = datetime.now() + timedelta(hours=8)
        mock_existing_shift.completed = False
        mock_existing_shift.status = "scheduled"
        mock_existing_shift.paid = False
        mock_repo.get_by_id.return_value = mock_existing_shift

        mock_updated_shift = MagicMock()
        mock_updated_shift.id = 1
        mock_updated_shift.pvz_id = 1
        mock_updated_shift.user_id = 1
        mock_updated_shift.starts_at = datetime.now()
        mock_updated_shift.ends_at = datetime.now() + timedelta(hours=8)
        mock_updated_shift.completed = True  # Только это поле обновлено
        mock_updated_shift.status = "scheduled"
        mock_updated_shift.paid = False
        mock_updated_shift.created_at = datetime.now()
        mock_updated_shift.updated_at = datetime.now()

        mock_repo.update.return_value = mock_updated_shift

        update_data = ScheduledShiftUpdateSchema(
            pvz_id=1,
            user_id=1,
            starts_at=datetime.now(),
            ends_at=datetime.now() + timedelta(hours=8),
            completed=True,
            status="scheduled",
            paid=False,
        )

        service = ScheduledShiftsService()
        result = await service.update_scheduled_shift(1, update_data, mock_repo)

        assert result.completed is True

        mock_repo.update.assert_called_once_with(
            id=1,
            pvz_id=1,
            user_id=1,
            starts_at=update_data.starts_at,
            ends_at=update_data.ends_at,
            completed=True,
            status="scheduled",
            paid=False,
        )

    async def test_update_scheduled_shift_not_found(self):
        """
        Тест на 404 при обновлении несуществующей смены.
        """
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None

        update_data = ScheduledShiftUpdateSchema(
            pvz_id=1,
            user_id=1,
            starts_at=datetime.now(),
            ends_at=datetime.now() + timedelta(hours=8),
            completed=False,
            status="scheduled",
            paid=False,
        )

        service = ScheduledShiftsService()

        with pytest.raises(HTTPException) as exc_info:
            await service.update_scheduled_shift(999, update_data, mock_repo)

        assert exc_info.value.status_code == 404
        assert "Смена не найдена" in str(exc_info.value.detail)

        mock_repo.update.assert_not_called()

    async def test_update_scheduled_shift_failed(self):
        """
        Тест на 400 при неудачном обновлении в репозитории.
        """
        mock_repo = AsyncMock()

        mock_existing_shift = MagicMock()
        mock_repo.get_by_id.return_value = mock_existing_shift
        mock_repo.update.return_value = None

        update_data = ScheduledShiftUpdateSchema(
            pvz_id=1,
            user_id=1,
            starts_at=datetime.now(),
            ends_at=datetime.now() + timedelta(hours=8),
            completed=True,
            status="completed",
            paid=True,
        )

        service = ScheduledShiftsService()

        with pytest.raises(HTTPException) as exc_info:
            await service.update_scheduled_shift(1, update_data, mock_repo)

        assert exc_info.value.status_code == 400
        assert "Невалидные параметры схемы" in str(exc_info.value.detail)

    async def test_delete_scheduled_shift_success(self):
        """
        Тест на успешное удаление смены.
        """
        mock_repo = AsyncMock()

        mock_shift = MagicMock()
        mock_shift.id = 1
        mock_repo.get_by_id.return_value = mock_shift
        mock_repo.delete.return_value = True

        service = ScheduledShiftsService()

        result = await service.delete_scheduled_shift(1, mock_repo)
        assert result is None

        mock_repo.delete.assert_called_once_with(1)

    async def test_delete_scheduled_shift_not_found(self):
        """
        Тест на 404 при удалении несуществующей смены.
        """
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None

        service = ScheduledShiftsService()

        with pytest.raises(HTTPException) as exc_info:
            await service.delete_scheduled_shift(999, mock_repo)

        assert exc_info.value.status_code == 404
        assert "Смена не найдена" in str(exc_info.value.detail)

        mock_repo.delete.assert_not_called()
