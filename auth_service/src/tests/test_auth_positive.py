import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


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
