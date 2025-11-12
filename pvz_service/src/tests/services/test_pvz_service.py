from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate
from src.services.pvz_service import PVZService
from src.utils.exceptions import (
    PVZAlreadyExistsException,
    PVZDeleteFailedException,
    PVZNotFoundException,
)

pytestmark = pytest.mark.asyncio


class TestPVZService:
    async def test_add_pvz_success(self):
        """
        Тест на успешное добавление ПВЗ, когда его еще нет в базе.
        """

        mock_repo = AsyncMock()

        mock_repo.get_pvz.return_value = None

        created_pvz_from_repo = MagicMock()
        created_pvz_from_repo.id = 1
        created_pvz_from_repo.code = "PVZ-123"
        created_pvz_from_repo.type = "ozon"
        created_pvz_from_repo.address = "г. Москва, ул. Ленина, 1"
        created_pvz_from_repo.owner_id = 10
        created_pvz_from_repo.group_id = 0
        created_pvz_from_repo.curator_id = 20
        created_pvz_from_repo.created_at = datetime.now()

        mock_repo.create.return_value = created_pvz_from_repo

        input_data = PVZAdd(
            code="PVZ-123",
            type="ozon",
            address="г. Москва, ул. Ленина, 1",
            owner_id=10,
            group_id=0,
            curator_id=20,
        )

        service = PVZService()
        result = await service.add_pvz(data=input_data, repo=mock_repo, group_repo=mock_repo)

        assert isinstance(result, PVZRead)
        assert result.id == 1
        assert result.code == "PVZ-123"

    async def test_add_pvz_conflict(self):
        """
        Тест на ошибку 409 Conflict, когда ПВЗ с таким кодом уже существует.
        """

        mock_repo = AsyncMock()
        mock_repo.get_pvz.return_value = MagicMock()

        input_data = PVZAdd(
            code="PVZ-123",
            type="ozon",
            address="addr",
            owner_id=1,
            group_id=0,
            curator_id=1,
        )

        service = PVZService()
        with pytest.raises(PVZAlreadyExistsException):
            await service.add_pvz(data=input_data, repo=mock_repo, group_repo=mock_repo)

        mock_repo.create.assert_not_called()

    async def test_update_pvz_by_id_success(self):
        """
        Тест на успешное обновление ПВЗ.
        """
        mock_repo = AsyncMock()

        mock_repo.get_pvz.return_value = MagicMock()

        updated_pvz_from_repo = MagicMock(
            id=1,
            code="OLD-CODE",
            created_at=datetime.now(),
            **{
                "address": "Новый адрес",
                "owner_id": 11,
                "curator_id": 22,
                "group_id": 1,
                "type": "wb",
            },
        )
        mock_repo.update.return_value = updated_pvz_from_repo

        input_data = PVZUpdate(address="Новый адрес", owner_id=11, curator_id=22, group_id=1)

        service = PVZService()
        result = await service.update_pvz_by_id(pvz_id=1, data=input_data, repo=mock_repo)

        assert result.address == "Новый адрес"
        assert result.owner_id == 11

    async def test_update_pvz_by_id_not_found(self):
        """
        Тест на ошибку 404 Not Found при обновлении.
        """
        mock_repo = AsyncMock()
        mock_repo.get_pvz.return_value = None

        input_data = PVZUpdate(address="any", owner_id=1, curator_id=1, group_id=0)

        service = PVZService()
        with pytest.raises(PVZNotFoundException):
            await service.update_pvz_by_id(pvz_id=999, data=input_data, repo=mock_repo)

        mock_repo.update.assert_not_called()

    async def test_get_pvz_by_id_success(self):
        """
        Тест на успешное получение ПВЗ по ID.
        """
        mock_repo = AsyncMock()

        found_pvz = MagicMock(
            id=1,
            code="PVZ-001",
            address="Some Address",
            created_at=datetime.now(),
            owner_id=1,
            group_id=0,
            curator_id=1,
            type="ozon",
        )
        mock_repo.get_pvz.return_value = found_pvz

        service = PVZService()
        result = await service.get_pvz_by_id(pvz_id=1, repo=mock_repo)

        assert result.id == 1
        assert result.code == "PVZ-001"

    async def test_get_pvz_by_id_not_found(self):
        """
        Тест на ошибку 404 Not Found при получении ПВЗ.
        """
        mock_repo = AsyncMock()
        mock_repo.get_pvz.return_value = None

        service = PVZService()
        with pytest.raises(PVZNotFoundException):
            await service.get_pvz_by_id(pvz_id=999, repo=mock_repo)

    async def test_get_pvzs_with_filters(self):
        """
        Тест на то, что get_pvzs правильно передает фильтры в DAO.
        """
        mock_repo = AsyncMock()
        mock_repo.get_pvzs.return_value = []

        service = PVZService()
        await service.get_pvzs(
            code="PVZ-007",
            type=None,
            address="г. Москва",
            repo=mock_repo,
        )

        expected_filters = {"code": "PVZ-007", "address": "г. Москва"}
        mock_repo.get_pvzs.assert_awaited_once_with(**expected_filters)

    async def test_delete_pvz_by_id_success(self):
        """
        Тест на успешное удаление ПВЗ.
        """
        mock_repo = AsyncMock()

        found_pvz = MagicMock(
            id=1,
            code="PVZ-TO-DELETE",
            address="...",
            created_at=datetime.now(),
            owner_id=1,
            group_id=0,
            curator_id=1,
            type="ozon",
        )
        mock_repo.get_pvz.return_value = found_pvz

        mock_repo.delete.return_value = True

        service = PVZService()
        result = await service.delete_pvz_by_id(pvz_id=1, repo=mock_repo)

        assert result["id"] == 1
        assert result["code"] == "PVZ-TO-DELETE"

    async def test_delete_pvz_by_id_not_found(self):
        """
        Тест на ошибку 404 при удалении несуществующего ПВЗ.
        """
        mock_repo = AsyncMock()
        mock_repo.get_pvz.return_value = None

        service = PVZService()
        with pytest.raises(PVZNotFoundException):
            await service.delete_pvz_by_id(pvz_id=999, repo=mock_repo)

        mock_repo.delete.assert_not_called()

    async def test_delete_pvz_by_id_dao_failure(self):
        """
        Тест на ошибку 500, если DAO не смог удалить запись.
        """
        mock_repo = AsyncMock()
        mock_repo.get_pvz.return_value = MagicMock()
        mock_repo.delete.return_value = False

        service = PVZService()
        with pytest.raises(PVZDeleteFailedException):
            await service.delete_pvz_by_id(pvz_id=1, repo=mock_repo)

        mock_repo.delete.assert_called_once()
