from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.enums import PositionSourceEnum
from src.tests.factories.permission_factories import PermissionFactory
from src.tests.factories.system_position_factories import SystemPositionFactory
from src.tests.factories.user_factories import (
    DEFAULT_PASSWORD,
    RegisterEmployeeFactory,
    ResetPasswordFactory,
    UserFactory,
    UserLoginFactory,
    UserPermissionFactory,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_override, expected_status, description",
    [
        ({"email": "not-an-email"}, 422, "invalid_email_format"),
        ({"password": "123"}, 422, "weak_password"),
        ({"email": ""}, 422, "empty_email"),
        ({"password": ""}, 422, "empty_password"),
    ],
    ids=lambda x: x if isinstance(x, str) else None,
)
async def test_register_validation_errors(
    client: AsyncClient,
    session: AsyncSession,
    payload_override: dict,
    expected_status: int,
    description: str,
):
    """Тест: Ошибки валидации при регистрации."""

    position = await SystemPositionFactory.create_with_permissions(session)

    base_payload = UserFactory.build(
        position_id=position.id,
        position_source=PositionSourceEnum.system,
    ).model_dump(mode="json")

    base_payload.update(payload_override)

    response = await client.post("/auth/register", json=base_payload)

    assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
async def test_register_duplicate_email(
    client: AsyncClient,
    session: AsyncSession,
):
    """Тест: Регистрация с уже существующим email."""

    existing_user = await UserFactory.create_async(session)
    position = await SystemPositionFactory.create_with_permissions(session)

    payload = UserFactory.build(
        email=existing_user.email,
        position_id=position.id,
        position_source=PositionSourceEnum.system,
    ).model_dump(mode="json")

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 409


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_override, expected_status, description",
    [
        (
            {"position_id": 99999, "position_source": PositionSourceEnum.system.value},
            404,
            "nonexistent_position",
        ),
        (
            {"position_id": None, "position_source": None, "register_token": None},
            422,
            "no_position_no_token",
        ),
        (
            {"position_id": None, "position_source": None, "register_token": "invalid.fake.token"},
            (400, 401),
            "invalid_register_token",
        ),
    ],
    ids=["nonexistent_position", "no_position_no_token", "invalid_register_token"],
)
async def test_register_business_logic_errors(
    client: AsyncClient,
    session: AsyncSession,
    payload_override: dict,
    expected_status: int | tuple,
    description: str,
):
    """Тест: Ошибки бизнес-логики при регистрации."""

    base_payload = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User",
    }

    base_payload.update(payload_override)

    response = await client.post("/auth/register", json=base_payload)

    if isinstance(expected_status, tuple):
        assert response.status_code in expected_status, f"Не удалось найти кейс: {description}"
    else:
        assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email, password, expected_status, description",
    [
        ("", "", 422, "empty_credentials"),
        ("", "SomePassword123!", 422, "empty_email"),
        ("test@example.com", "", 422, "empty_password"),
        ("nonexistent@example.com", "SomePassword123!", 404, "nonexistent_email"),
    ],
    ids=["empty_credentials", "empty_email", "empty_password", "nonexistent_email"],
)
async def test_login_errors_no_user_required(
    client: AsyncClient,
    session: AsyncSession,
    email: str,
    password: str,
    expected_status: int,
    description: str,
):
    """Тест: Ошибки логина (без необходимости создания пользователя)."""

    payload = {"email": email, "password": password}

    response = await client.post("/auth/login", json=payload)

    assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"
    assert "access_token" not in response.cookies


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "password, expected_status, description",
    [
        ("WrongPassword123!", 401, "wrong_password"),
    ],
    ids=["wrong_password"],
)
async def test_login_errors_with_user(
    client: AsyncClient,
    session: AsyncSession,
    password: str,
    expected_status: int | tuple,
    description: str,
):
    """Тест: Ошибки логина (с созданием пользователя)."""

    user = await UserFactory.create_async(session)

    payload = UserLoginFactory.build(
        email=user.email,
        password=password,
    ).model_dump(mode="json")

    response = await client.post("/auth/login", json=payload)

    if isinstance(expected_status, tuple):
        assert response.status_code in expected_status, f"Не удалось найти кейс: {description}"
    else:
        assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cookie_value, expected_status, description",
    [
        (None, 401, "no_cookies"),
        ("invalid.fake.token", 401, "invalid_token"),
        ("", 401, "empty_token"),
    ],
    ids=["no_cookies", "invalid_token", "empty_token"],
)
async def test_refresh_token_errors(
    client: AsyncClient,
    session: AsyncSession,
    cookie_value: str | None,
    expected_status: int,
    description: str,
):
    """Тест: Ошибки обновления токена."""

    if cookie_value is not None:
        client.cookies.set("refresh_token", cookie_value)

    response = await client.post("/auth/refresh_token")

    assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
async def test_refresh_token_with_access_token_instead(
    client: AsyncClient,
    session: AsyncSession,
):
    """Тест: Попытка использовать access_token вместо refresh_token."""

    user = await UserFactory.create_async(session)

    login_response = await client.post(
        "/auth/login",
        json=UserLoginFactory.build(
            email=user.email,
            password=DEFAULT_PASSWORD,
        ).model_dump(mode="json"),
    )
    assert login_response.status_code == 200

    access_token = login_response.cookies.get("access_token")
    client.cookies.set("refresh_token", access_token)

    response = await client.post("/auth/refresh_token")

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "owner_exists, position_exists, expected_status",
    [
        (False, True, 404),
        (True, False, 404),
        (False, False, 404),
    ],
    ids=["invalid_owner", "invalid_position", "both_invalid"],
)
async def test_generate_register_token_errors(
    client: AsyncClient,
    session: AsyncSession,
    owner_exists: bool,
    position_exists: bool,
    expected_status: int,
):
    """Тест: Ошибки генерации токена регистрации."""

    owner_id = (await UserFactory.create_async(session)).id if owner_exists else 99999
    position_id = (await SystemPositionFactory.create_async(session)).id if position_exists else 99999

    payload = RegisterEmployeeFactory.build(
        owner_id=owner_id,
        position_id=position_id,
        pvz_id=1,
    ).model_dump(mode="json")

    response = await client.post("/auth/generate_register_token", json=payload)

    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email, expected_status, description",
    [
        ("not-an-email", 422, "invalid_format"),
        ("", 422, "empty_email"),
        ("nonexistent@example.com", 200, "nonexistent_email"),
    ],
    ids=["invalid_format", "empty_email", "nonexistent_email"],
)
async def test_forgot_password_errors(
    client: AsyncClient,
    session: AsyncSession,
    email: str,
    expected_status: int,
    description: str,
):
    """Тест: Ошибки запроса восстановления пароля."""

    payload = {"email": email}

    response = await client.post("/auth/forgot_password", json=payload)

    assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
async def test_reset_password_invalid_token(
    client: AsyncClient,
    session: AsyncSession,
):
    """Тест: Сброс пароля с невалидным токеном."""

    payload = ResetPasswordFactory.build(token="invalid.reset.token").model_dump(mode="json")

    response = await client.post("/auth/reset_password", json=payload)

    assert response.status_code in (400, 401)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token_used, token_expired, new_password, expected_status, description",
    [
        (False, True, "ValidPassword123!", (400, 401), "expired_token"),
        (True, False, "ValidPassword123!", 401, "used_token"),
        (False, False, "123", 422, "weak_password"),
        (False, False, "", 422, "empty_password"),
    ],
    ids=["expired_token", "used_token", "weak_password", "empty_password"],
)
async def test_reset_password_with_mocked_token(
    client: AsyncClient,
    session: AsyncSession,
    mocker,
    token_used: bool,
    token_expired: bool,
    new_password: str,
    expected_status: int | tuple,
    description: str,
):
    """Тест: Ошибки сброса пароля с мокированным токеном."""

    user = await UserFactory.create_async(session)

    if token_expired:
        expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
    else:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    mock_token_data = MagicMock()
    mock_token_data.user_id = user.id
    mock_token_data.email = user.email
    mock_token_data.used = token_used
    mock_token_data.expires_at = expires_at

    mocker.patch(
        "src.services.token_service.StatefulTokenService.get_reset_token_data",
        return_value=mock_token_data,
    )

    payload = {
        "token": "mocked-valid-token",
        "new_password": new_password,
        "confirm_new_password": new_password,
    }

    response = await client.post("/auth/reset_password", json=payload)

    if isinstance(expected_status, tuple):
        assert response.status_code in expected_status, f"Не удалось найти кейс: {description}"
    else:
        assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
async def test_authorize_without_login(
    client: AsyncClient,
    session: AsyncSession,
):
    """Тест: Авторизация без логина."""

    response = await client.post(
        "/auth/authorize",
        params={"permission": "dashboard:view"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_authorize_missing_permission_param(
    client: AsyncClient,
    session: AsyncSession,
):
    """Тест: Авторизация без параметра permission."""

    user = await UserFactory.create_async(session)

    await client.post(
        "/auth/login",
        json=UserLoginFactory.build(
            email=user.email,
            password=DEFAULT_PASSWORD,
        ).model_dump(mode="json"),
    )

    response = await client.post("/auth/authorize")

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_permissions, required_permission, expected_status, description",
    [
        ([], "any:permission", 403, "no_permissions"),
        (["users:read"], "admin:delete", 403, "wrong_permission"),
        (["users:read", "users:write"], "admin:full", 403, "multiple_but_missing"),
    ],
    ids=["no_permissions", "wrong_permission", "multiple_but_missing"],
)
async def test_authorize_permission_denied(
    client: AsyncClient,
    session: AsyncSession,
    user_permissions: list[str],
    required_permission: str,
    expected_status: int,
    description: str,
):
    """Тест: Отказ в авторизации из-за отсутствия права."""

    user = await UserFactory.create_async(session)

    for perm_code in user_permissions:
        permission = await PermissionFactory.create_async(
            session,
            code_name=perm_code,
        )
        await UserPermissionFactory.create_async(
            session,
            user_id=user.id,
            permission_id=permission.id,
        )

    await client.post(
        "/auth/login",
        json=UserLoginFactory.build(
            email=user.email,
            password=DEFAULT_PASSWORD,
        ).model_dump(mode="json"),
    )

    response = await client.post(
        "/auth/authorize",
        params={"permission": required_permission},
    )

    assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "is_logged_in, expected_status, description",
    [
        (False, (200, 401), "logout_without_login"),
        (True, 200, "normal_logout"),
    ],
    ids=["without_login", "normal"],
)
async def test_logout_scenarios(
    client: AsyncClient,
    session: AsyncSession,
    is_logged_in: bool,
    expected_status: int | tuple,
    description: str,
):
    """Тест: Различные сценарии logout."""

    if is_logged_in:
        user = await UserFactory.create_async(session)
        await client.post(
            "/auth/login",
            json=UserLoginFactory.build(
                email=user.email,
                password=DEFAULT_PASSWORD,
            ).model_dump(mode="json"),
        )

    response = await client.post("/auth/logout")

    if isinstance(expected_status, tuple):
        assert response.status_code in expected_status, f"Не удалось найти кейс: {description}"
    else:
        assert response.status_code == expected_status, f"Не удалось найти кейс: {description}"


@pytest.mark.asyncio
async def test_double_logout_idempotency(
    client: AsyncClient,
    session: AsyncSession,
):
    """Тест: Двойной logout должен быть идемпотентным."""

    user = await UserFactory.create_async(session)

    await client.post(
        "/auth/login",
        json=UserLoginFactory.build(
            email=user.email,
            password=DEFAULT_PASSWORD,
        ).model_dump(mode="json"),
    )

    response1 = await client.post("/auth/logout")
    assert response1.status_code == 200

    response2 = await client.post("/auth/logout")
    assert response2.status_code in (200, 401)
