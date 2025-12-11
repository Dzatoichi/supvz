import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.database.base import Base, db_helper
from src.main import app
from src.settings.config import Settings

test_settings = Settings(_env_file=".env.test")
TEST_DATABASE_URL = test_settings.CONNECT_ASYNC()

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, echo=False)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Создание таблиц"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def session():
    """
    Создает сессию
    """
    connection = await test_engine.connect()
    transaction = await connection.begin()

    session = TestingSessionLocal(bind=connection)

    async def mock_commit():
        await session.flush()

    session.commit = mock_commit

    async def mock_close():
        pass

    session.close = mock_close

    class MockTransactionContext:
        async def __aenter__(self):
            return None

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def mock_begin():
        return MockTransactionContext()

    session.begin = mock_begin

    class MockSessionMaker:
        def __call__(self):
            return self

        async def __aenter__(self):
            return session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    original_maker = db_helper.async_session_maker
    db_helper.async_session_maker = MockSessionMaker()

    async def override_session_getter():
        yield session

    if hasattr(db_helper, "session_getter"):
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
