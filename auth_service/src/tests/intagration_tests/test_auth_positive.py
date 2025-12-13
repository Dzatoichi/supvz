from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.position_permissions.system_position_permissions import SystemPositionPermissions
from src.models.users.users import Users
from src.schemas.enums import PositionSourceEnum
from src.tests.factories.permission_factories import PermissionFactory
from src.tests.factories.system_position_factories import SystemPositionFactory
from src.tests.factories.user_factories import (
    DEFAULT_PASSWORD,
    ForgotPasswordFactory,
    RegisterEmployeeFactory,
    ResetPasswordFactory,
    UserFactory,
    UserLoginFactory,
    UserPermissionFactory,
)


@pytest.mark.asyncio
async def test_register_user_system_position(
    client,
    session,
):
    """
    Тест: Успешная регистрация через position_id + position_source.
    POST /auth/register

    Сценарий:
    1. В БД заранее создается системная должность и право.
    2. Отправляем запрос на регистрацию с ID этой должности.
    3. Проверяем, что пользователь создан и возвращен корректный ответ.
    """
    position = await SystemPositionFactory.create_with_permissions(session)

    payload_schema = UserFactory.build(
        position_id=position.id,
        position_source=PositionSourceEnum.system,
    )
    payload = payload_schema.model_dump(mode="json")

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 201
    resp_data = response.json()
    assert resp_data["email"] == payload["email"]

    stmt = select(Users).where(Users.email == payload["email"])
    result = await session.execute(stmt)
    created_user = result.scalar_one_or_none()
    assert created_user is not None


@pytest.mark.asyncio
async def test_register_employee_with_token(
    client: AsyncClient,
    session: AsyncSession,
):
    """
    Тест: Регистрация сотрудника через register_token.

    Проверки:
    1. HTTP 200/201.
    2. Юзер создан в БД.
    3. Юзеру скопированы права (permissions) от должности (position), указанной при генерации токена.
    """
    owner = await UserFactory.create_async(session)
    position = await SystemPositionFactory.create_with_permissions(session)

    expected_perms_stmt = select(SystemPositionPermissions.permission_id).where(
        SystemPositionPermissions.system_position_id == position.id
    )
    result = await session.execute(expected_perms_stmt)
    expected_permission_ids = set(result.scalars().all())

    token_payload = RegisterEmployeeFactory.build(
        owner_id=owner.id,
        position_id=position.id,
        pvz_id=1,
    )
    payload = token_payload.model_dump(mode="json")

    token_response = await client.post(
        "/auth/generate_register_token",
        json=payload,
    )

    assert token_response.status_code == 200
    register_token = token_response.json()["register_token"]

    payload_schema = UserFactory.build(
        register_token=register_token,
        position_id=None,
        position_source=None,
    )
    payload = payload_schema.model_dump(mode="json")

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]

    query = select(Users).options(selectinload(Users.permission_links)).where(Users.email == payload["email"])
    result = await session.execute(query)
    created_user = result.scalar_one_or_none()

    assert created_user is not None

    user_permission_ids = {perm.permission_id for perm in created_user.permission_links}

    assert user_permission_ids == expected_permission_ids, (
        f"Права пользователя не совпадают с правами должности.\n"
        f"Ожидали: {expected_permission_ids}\n"
        f"Получили: {user_permission_ids}"
    )


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, session: AsyncSession):
    """
    Тест: Успешная аутентификация пользователя.
    POST /auth/login

    Сценарий:
    1. Создаем пользователя в БД (с известным паролем).
    2. Отправляем креды.
    3. Проверяем установку cookies.
    """
    user = await UserFactory.create_async(session)

    payload = UserLoginFactory.build(
        email=user.email,
        password=DEFAULT_PASSWORD,
    ).model_dump(mode="json")

    response = await client.post(
        "/auth/login",
        json=payload,
    )

    assert response.status_code == 200

    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert len(response.cookies["access_token"]) > 0
    assert len(response.cookies["refresh_token"]) > 0


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, session: AsyncSession):
    """
    Тест: Обновление токенов.
    POST /auth/refresh_token
    """
    user = await UserFactory.create_async(session)

    login_payload = UserLoginFactory.build(
        email=user.email,
        password=DEFAULT_PASSWORD,
    )
    login_response = await client.post(
        "/auth/login",
        json=login_payload.model_dump(mode="json"),
    )
    assert login_response.status_code == 200

    old_access_token = login_response.cookies.get("access_token")

    response = await client.post("/auth/refresh_token")

    assert response.status_code == 200

    new_access_token = response.cookies.get("access_token")
    new_refresh_token = response.cookies.get("refresh_token")

    assert new_access_token is not None
    assert new_refresh_token is not None
    assert new_access_token != old_access_token


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, session: AsyncSession):
    """
    Тест: Выход из системы.
    POST /auth/logout
    """
    user = await UserFactory.create_async(session)

    login_payload = UserLoginFactory.build(
        email=user.email,
        password=DEFAULT_PASSWORD,
    )
    login_response = await client.post(
        "/auth/login",
        json=login_payload.model_dump(mode="json"),
    )
    assert login_response.status_code == 200

    access_token = login_response.cookies.get("access_token")
    refresh_token = login_response.cookies.get("refresh_token")

    assert access_token is not None and refresh_token is not None

    response = await client.post("/auth/logout")
    assert response.status_code == 200

    del_access_token = response.cookies.get("access_token")
    del_refresh_token = response.cookies.get("refresh_token")

    assert del_access_token is None and del_refresh_token is None


@pytest.mark.asyncio
async def test_generate_register_token_success(client, session):
    """
    Тест: Генерация токена для регистрации сотрудника.
    POST /auth/generate_register_token
    """
    owner = await UserFactory.create_async(session)
    position = await SystemPositionFactory.create_async(session)

    payload = RegisterEmployeeFactory.build(
        owner_id=owner.id,
        position_id=position.id,
        pvz_id=1,
    ).model_dump(mode="json")

    response = await client.post(
        "/auth/generate_register_token",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()
    assert "register_token" in data
    assert len(data["register_token"]) > 0


@pytest.mark.asyncio
async def test_forgot_password(client, session):
    """
    Тест: Запрос на восстановление пароля.
    POST /auth/forgot_password
    """
    user = await UserFactory.create_async(session)
    payload = ForgotPasswordFactory.build(email=user.email).model_dump(mode="json")

    response = await client.post(
        "/auth/forgot_password",
        json=payload,
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_reset_password_success(client, session, mocker):
    """
    Тест: Успешный сброс пароля по токену.
    POST /auth/reset_password
    """
    user = await UserFactory.create_async(session)

    mock_token_data = MagicMock()
    mock_token_data.user_id = user.id
    mock_token_data.email = user.email
    mock_token_data.used = False
    mock_token_data.expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    mocker.patch(
        "src.services.token_service.StatefulTokenService.get_reset_token_data",
        return_value=mock_token_data,
    )

    payload = ResetPasswordFactory.build().model_dump(mode="json")

    response = await client.post(
        "/auth/reset_password",
        json=payload,
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_authorize_with_permission(client, session):
    """
    Тест: Авторизация пользователя с нужным permission.
    POST auth/authorize
    """
    user = await UserFactory.create_async(session)
    permission = await PermissionFactory.create_async(
        session,
        code_name="dashboard:view",
        description="Dashboard",
    )
    await UserPermissionFactory.create_async(
        session,
        user_id=user.id,
        permission_id=permission.id,
    )

    login_payload = UserLoginFactory.build(
        email=user.email,
        password=DEFAULT_PASSWORD,
    )

    await client.post(
        "/auth/login",
        json=login_payload.model_dump(mode="json"),
    )

    response = await client.post(
        "/auth/authorize",
        params={"permission": "dashboard:view"},
    )

    assert response.status_code == 200
