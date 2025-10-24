import os

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

if os.path.exists(".env.test"):
    load_dotenv(".env.test", override=True)
else:
    load_dotenv(".env", override=True)

from src.main import app
from src.tests.services.fake_pvz_service import FakePVZService
from src.utils.dependencies import get_pvzs_service


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_pvzs_service] = lambda: FakePVZService()
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
