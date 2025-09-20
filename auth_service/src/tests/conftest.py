import os

import pytest
from dotenv import load_dotenv

if os.path.exists('.env.test'):
    load_dotenv('.env.test', override=True)
else:
    load_dotenv('.env', override=True)

from src.main import app
from src.tests.fake_services import FakeAuthService, FakeJWTTokensService, FakeStatefulTokenService, FakeUsersDAO
from src.utils.dependencies import get_auth_service, get_jwt_tokens_service, get_stateful_token_service, get_users_dao


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()
    app.dependency_overrides[get_users_dao] = lambda: FakeUsersDAO()
    app.dependency_overrides[get_jwt_tokens_service] = lambda: FakeJWTTokensService()
    app.dependency_overrides[get_stateful_token_service] = lambda: FakeStatefulTokenService()
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
