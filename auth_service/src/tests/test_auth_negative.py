import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app

transport = ASGITransport(app=app)


@pytest.mark.anyio
async def test_register_user_passwords_do_not_match():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "password": "12345678",
            "confirm_password": "87654321",
            "name": "Test User",
            "phone_number": "+1234567890"
        })
    assert response.status_code == 422
    assert "Passwords do not match" in response.text


@pytest.mark.anyio
async def test_register_user_invalid_email():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "not-an-email",
            "username": "testuser",
            "password": "12345678",
            "confirm_password": "12345678",
            "name": "Test",
            "phone_number": "+1234567890"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_user_short_password():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "123",  # Слишком короткий
            "confirm_password": "123",
            "name": "Test",
            "phone_number": "+1234567890"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_user_invalid_phone():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "12345678",
            "confirm_password": "12345678",
            "name": "Test",
            "phone_number": "1234567890"  # Нет "+"
        })
    assert response.status_code == 422
    assert "Номер телефона должен начинаться с" in response.text


@pytest.mark.anyio
async def test_register_user_missing_required_field():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "12345678",
            "name": "Test",
            "phone_number": "+1234567890"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_invalid_email():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email": "not-an-email",
            "password": "12345678"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_missing_password():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email": "test@example.com"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_forgot_password_invalid_email():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/forgot_password", json={
            "email": "not-an-email"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_reset_password_passwords_do_not_match():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/reset_password", json={
            "token": "sometoken",
            "new_password": "newpassword123",
            "confirm_new_password": "otherpassword"
        })
    assert response.status_code == 422
    assert "Passwords do not match" in response.text


@pytest.mark.anyio
async def test_reset_password_missing_token():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/reset_password", json={
            "new_password": "newpassword123",
            "confirm_new_password": "newpassword123"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_logout_missing_refresh_token():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/logout", json={
            "access_token": "access"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_logout_missing_access_token():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/logout", json={
            "refresh_token": "refresh"
        })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_refresh_token_missing_token():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/refresh_token", json={})
    assert response.status_code == 422
