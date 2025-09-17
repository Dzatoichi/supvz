import os

import pytest
from dotenv import load_dotenv


def pytest_configure():
    # Если есть .env.test — грузим его, иначе обычный .env
    if os.path.exists('.env.test'):
        load_dotenv('.env.test', override=True)
    else:
        load_dotenv('.env', override=True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
