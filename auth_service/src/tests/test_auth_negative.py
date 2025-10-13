import pytest


@pytest.mark.anyio
async def test_register_user_passwords_do_not_match(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "12345678",
            "confirm_password": "87654321",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_user_invalid_email(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "username": "testuser",
            "password": "12345678",
            "confirm_password": "12345678",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_user_short_password(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "123",
            "confirm_password": "123",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_user_invalid_phone(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "12345678",
            "confirm_password": "12345678",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_user_missing_required_field(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "12345678",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_invalid_email(client):
    response = await client.post(
        "/auth/login", json={"email": "not-an-email", "password": "12345678"}
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_missing_password(client):
    response = await client.post("/auth/login", json={"email": "test@example.com"})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_forgot_password_invalid_email(client):
    response = await client.post(
        "/auth/forgot_password", json={"email": "not-an-email"}
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_reset_password_passwords_do_not_match(client):
    response = await client.post(
        "/auth/reset_password",
        json={
            "token": "sometoken",
            "new_password": "newpassword123",
            "confirm_new_password": "otherpassword",
        },
    )
    assert response.status_code == 422
    assert "Passwords do not match" in response.text


@pytest.mark.anyio
async def test_reset_password_missing_token(client):
    response = await client.post(
        "/auth/reset_password",
        json={
            "new_password": "newpassword123",
            "confirm_new_password": "newpassword123",
        },
    )
    assert response.status_code == 422
