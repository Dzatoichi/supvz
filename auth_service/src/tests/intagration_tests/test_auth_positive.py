import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_permissions.user_permissions import UserPermissions
from src.tests.factories.user_factories import (
    UserFactory,
    UserLoginPayloadFactory,
    UserRegisterEmployeePayloadFactory,
    UserRegisterPayloadFactory,
)


@pytest.mark.asyncio
async def test_register_user_system_position(
    client,
    session,
    system_position_with_permissions,
):
    """
    Тест: Успешная регистрация пользователя на системную должность.
    POST /auth/register

    Сценарий:
    1. В БД заранее создается системная должность и право.
    2. Отправляем запрос на регистрацию с ID этой должности.
    3. Проверяем, что пользователь создан и возвращен корректный ответ.
    """
    position, perms = await system_position_with_permissions(perms_count=3)

    payload_model = UserRegisterPayloadFactory.build(
        position_id=position.id,
        position_source="system",
    )
    payload = payload_model.model_dump(mode="json")

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]

    stmt = select(func.count()).select_from(UserPermissions).where(UserPermissions.user_id == data["id"])

    count = await session.scalar(stmt)
    assert count == 3, "Пользователю должны были присвоиться 3 права от должности"


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
    password = "StrongPassword123!"
    user = await UserFactory.create(session, password=password)

    payload = UserLoginPayloadFactory.build(
        email=user.email,
        password=password,
    ).model_dump(mode="json")

    response = await client.post("/auth/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, session: AsyncSession):
    """
    Тест: Обновление токенов.
    POST /auth/refresh_token
    """
    password = "Password123!"
    user = await UserFactory.create(session, password=password)

    login_payload = UserLoginPayloadFactory.build(email=user.email, password=password).model_dump(mode="json")

    login_response = await client.post("/auth/login", json=login_payload)

    refresh_token_cookie = login_response.cookies["refresh_token"]
    client.cookies.set("refresh_token", refresh_token_cookie)

    response = await client.post("/auth/refresh_token")

    assert response.status_code == 200

    assert "access_token" in response.cookies
    assert response.cookies["access_token"] != ""


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, session: AsyncSession):
    """
    Тест: Выход из системы.
    POST /auth/logout
    """
    password = "Password123!"
    user = await UserFactory.create(session, password=password)
    login_payload = UserLoginPayloadFactory.build(email=user.email, password=password).model_dump(mode="json")
    await client.post("/auth/login", json=login_payload)

    response = await client.post("/auth/logout")

    assert response.status_code == 200

    assert "access_token" not in response.cookies or response.cookies["access_token"] == ""


@pytest.mark.asyncio
async def test_generate_register_token(client: AsyncClient, session: AsyncSession):
    """
    Тест: Генерация токена регистрации для сотрудника.
    POST /auth/generate_register_token
    """
    owner = await UserFactory.create(session)

    payload_model = UserRegisterEmployeePayloadFactory.build(
        owner_id=owner.id,
    )
    payload = payload_model.model_dump(mode="json")

    response = await client.post("/auth/generate_register_token", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "register_token" in data
    assert len(data["register_token"]) > 0


@pytest.mark.asyncio
async def test_forgot_password(client: AsyncClient, session: AsyncSession):
    """
    Тест: Запрос на восстановление пароля.
    POST /auth/forgot_password
    """
    user = await UserFactory.create(session)

    payload = {"email": user.email}

    response = await client.post("/auth/forgot_password", json=payload)

    assert response.status_code == 200
