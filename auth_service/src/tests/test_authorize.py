import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from src.services.auth_service import AuthService
from src.core.security.permissions import PermissionEnum


@pytest.mark.asyncio
async def test_authorize_user_success():
    """Тест успешной авторизации"""

    # Мокируем зависимости
    mock_token_service = AsyncMock()
    mock_token_service.validate_token.return_value = {
        "user_id": 1,
        "email": "test@example.com"
    }

    mock_users_dao = AsyncMock()
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    mock_user.role = "owner"
    mock_user.is_active = True
    mock_users_dao.get_user_by_id.return_value = mock_user

    # Создаем сервис с моками
    auth_service = AuthService(
        users_dao=mock_users_dao,
        token_service=mock_token_service
    )

    # Мок credentials
    class MockCredentials:
        def __init__(self, token):
            self.credentials = token

    credentials = MockCredentials("valid_token")

    # Вызываем метод
    role, permissions = await auth_service.authorize_user(credentials)

    # Проверяем результаты
    assert role == "owner"
    assert isinstance(permissions, list)
    assert len(permissions) > 0
    assert PermissionEnum.VIEW_DASHBOARD in permissions
    assert PermissionEnum.MANAGE_SYSTEM_SETTINGS in permissions


@pytest.mark.asyncio
async def test_authorize_user_invalid_token():
    """Тест с невалидным токеном"""

    mock_token_service = AsyncMock()
    mock_token_service.validate_token.side_effect = Exception("Invalid token")

    # Создаем сервис с моком token_service
    auth_service = AuthService(token_service=mock_token_service)

    class MockCredentials:
        def __init__(self, token):
            self.credentials = token

    credentials = MockCredentials("invalid_token")

    # Проверяем, что выбрасывается исключение
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.authorize_user(credentials)

    assert exc_info.value.status_code == 401
    assert "Invalid or expired token" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_authorize_user_inactive():
    """Тест с неактивным пользователем"""

    mock_token_service = AsyncMock()
    mock_token_service.validate_token.return_value = {
        "user_id": 1,
        "email": "test@example.com"
    }

    mock_users_dao = AsyncMock()
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.is_active = False  # Неактивный пользователь
    mock_users_dao.get_user_by_id.return_value = mock_user

    # Создаем сервис с моками
    auth_service = AuthService(
        users_dao=mock_users_dao,
        token_service=mock_token_service
    )

    class MockCredentials:
        def __init__(self, token):
            self.credentials = token

    credentials = MockCredentials("valid_token")

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.authorize_user(credentials)

    assert exc_info.value.status_code == 401
    assert "User not found or inactive" in str(exc_info.value.detail)


if __name__ == "__main__":
    import asyncio


    async def run_all_tests():
        try:
            await test_authorize_user_success()
            await test_authorize_user_invalid_token()
            await test_authorize_user_inactive()
            print("🎉 All tests passed!")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise


    asyncio.run(run_all_tests())