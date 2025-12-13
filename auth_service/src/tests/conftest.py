import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from src.database.base import Base, db_helper
from src.main import app
from src.settings.config import Settings
from src.tests.factories.permission_factories import PermissionFactory
from src.tests.factories.system_position_factories import SystemPositionFactory, SystemPositionPermissionLinkFactory

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

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async def mock_close():
        pass

    session.close = mock_close

    class MockSessionManager:
        async def __aenter__(self):
            return session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    original_maker = db_helper.async_session_maker
    db_helper.async_session_maker = lambda: MockSessionManager()

    async def override_session_getter():
        yield session

    app.dependency_overrides[db_helper.session_getter] = override_session_getter

    yield session

    db_helper.async_session_maker = original_maker
    app.dependency_overrides.clear()

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


@pytest.fixture
async def system_position_with_permissions(session: AsyncSession):
    async def _create(perms_count: int = 2):
        position = await SystemPositionFactory.create_async(session)
        perms = []
        for _ in range(perms_count):
            perm = await PermissionFactory.create_async(session)
            perms.append(perm)
            await SystemPositionPermissionLinkFactory.create_async(
                session,
                system_position_id=position.id,
                permission_id=perm.id,
            )
        await session.flush()
        return position, perms

    return _create
