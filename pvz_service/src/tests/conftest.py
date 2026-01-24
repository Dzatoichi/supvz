import uuid
from contextlib import asynccontextmanager

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
    Создает сессию с поддержкой реальных commit/rollback,
    но всё откатывается в конце теста.

    Ключ: join_transaction_mode="create_savepoint"
    """
    connection = await test_engine.connect()
    transaction = await connection.begin()

    TestSessionLocal = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        autoflush=False,
        join_transaction_mode="create_savepoint",
    )

    session = TestSessionLocal()

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


def create_auth_headers(user_id: int) -> dict[str, str]:
    """Создаёт заголовки авторизации для указанного пользователя."""
    return {
        "X-Internal-API-Key": test_settings.INTERNAL_API_KEY,
        "X-User-ID": str(user_id),
    }


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Заголовки для авторизованных запросов (дефолтный пользователь)."""
    return create_auth_headers(TEST_OWNER_ID)


class EventIdClient:
    """
    Обёртка над AsyncClient, автоматически добавляющая X-Idempotency-Key
    для мутирующих запросов (POST, PATCH, PUT, DELETE).
    """

    def __init__(self, client: AsyncClient):
        self._client = client

    def _merge_headers_with_event_id(self, headers: dict | None) -> dict:
        """Добавляет уникальный event_id к headers."""
        result = dict(headers) if headers else {}
        result["X-Idempotency-Key"] = str(uuid.uuid4())
        return result

    async def get(self, url: str, **kwargs):
        """GET запросы не требуют event_id."""
        return await self._client.get(url, **kwargs)

    async def post(self, url: str, **kwargs):
        kwargs["headers"] = self._merge_headers_with_event_id(kwargs.get("headers"))
        return await self._client.post(url, **kwargs)

    async def patch(self, url: str, **kwargs):
        kwargs["headers"] = self._merge_headers_with_event_id(kwargs.get("headers"))
        return await self._client.patch(url, **kwargs)

    async def put(self, url: str, **kwargs):
        kwargs["headers"] = self._merge_headers_with_event_id(kwargs.get("headers"))
        return await self._client.put(url, **kwargs)

    async def delete(self, url: str, **kwargs):
        kwargs["headers"] = self._merge_headers_with_event_id(kwargs.get("headers"))
        return await self._client.delete(url, **kwargs)


@pytest.fixture(scope="function")
async def client(session, auth_headers: dict[str, str]) -> EventIdClient:
    """HTTP клиент с автоматическим добавлением idempotency key."""
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers=auth_headers,
    ) as ac:
        yield EventIdClient(ac)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def make_auth_headers():
    """Фабрика заголовков для разных пользователей."""
    return create_auth_headers(TEST_OWNER_ID)


@pytest.fixture
def make_client_for_user(session):
    """Фабрика клиентов для разных пользователей."""

    @asynccontextmanager
    async def _make(user_id: int):
        headers = create_auth_headers(user_id)
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
            headers=headers,
        ) as ac:
            yield EventIdClient(ac)

    return _make
