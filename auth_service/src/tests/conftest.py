import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.database.base import Base, db_helper
from src.main import app
from src.settings.config import Settings
from src.tests.fixtures.permissions import *  # noqa: F403
from src.tests.fixtures.positions import *  # noqa: F403

test_settings = Settings(_env_file=".env.test")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine(event_loop):
    engine = create_async_engine(test_settings.CONNECT_ASYNC(), poolclass=NullPool, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def session(engine):
    connection = await engine.connect()
    transaction = await connection.begin()

    TestSessionLocal = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        autoflush=False,
    )

    session = TestSessionLocal()

    session.begin = session.begin_nested

    async def mock_commit():
        await session.flush()

    session.commit = mock_commit

    class MockSessionManager:
        def __call__(self):
            return self

        async def __aenter__(self):
            return session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    original_maker = db_helper.async_session_maker
    db_helper.async_session_maker = MockSessionManager()

    async def override_session_getter():
        yield session

    app.dependency_overrides[db_helper.session_getter] = override_session_getter

    yield session

    db_helper.async_session_maker = original_maker
    app.dependency_overrides.clear()

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture(scope="function")
async def client(session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
