import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.tests.fake_services import FakeAuthService, FakeJWTTokensService, FakeStatefulTokenService, FakeUsersDAO
from src.utils.dependencies import (
    get_auth_service,
    get_jwt_tokens_service,
    get_stateful_token_service,
    get_users_dao,
)


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()
    app.dependency_overrides[get_users_dao] = lambda: FakeUsersDAO()
    app.dependency_overrides[get_jwt_tokens_service] = lambda: FakeJWTTokensService()
    app.dependency_overrides[get_stateful_token_service] = lambda: FakeStatefulTokenService()
    yield
    app.dependency_overrides = {}


@pytest.mark.anyio
async def test_register_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "password": "12345678",
            "confirm_password": "12345678",
            "name": "Test User",
            "phone_number": "+1234567890"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"


@pytest.mark.anyio
async def test_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email": "test@example.com",
            "password": "12345678"
        })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.anyio
async def test_forgot_password():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/forgot_password", json={
            "email": "test@example.com"
        })
    assert response.status_code == 200


@pytest.mark.anyio
async def test_reset_password():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/reset_password", json={
            "token": "sometoken",
            "new_password": "newpassword123",
            "confirm_new_password": "newpassword123"
        })
    assert response.status_code == 200


@pytest.mark.anyio
async def test_logout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/logout", json={
            "refresh_token": "refresh_token_new_shma",
            "access_token": "access_token_new_shma"
        })
    assert response.status_code == 200


@pytest.mark.anyio
async def test_refresh_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/refresh_token", params={
            "refresh_token": "new_refresh_token",
        })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
