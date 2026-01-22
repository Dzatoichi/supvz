import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.database.base import Base, db_helper
from src.main import app
from src.settings.config import Settings, settings

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


# ID тестового пользователя-владельца
TEST_OWNER_ID = 999999


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Заголовки для авторизованных запросов."""
    return {
        "X-Internal-API-Key": settings.INTERNAL_API_KEY,
        "X-User-ID": str(TEST_OWNER_ID),
    }


@pytest.fixture(scope="function")
async def client(session, auth_headers: dict[str, str]):
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers=auth_headers,
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# Если нужен клиент с другим user_id
@pytest.fixture
def make_auth_headers():
    """Фабрика заголовков для разных пользователей."""

    def _make(user_id: int) -> dict[str, str]:
        return {
            "X-Internal-API-Key": test_settings.INTERNAL_API_KEY,
            "X-User-ID": str(user_id),
        }

    return _make
