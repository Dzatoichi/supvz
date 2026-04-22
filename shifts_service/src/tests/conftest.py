from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.database.base import Base
from src.main import app
from src.settings.config import Settings
from src.utils.dependencies import get_session

test_settings = Settings(_env_file=".env.test")
TEST_DATABASE_URL = test_settings.CONNECT_ASYNC()

_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, echo=False)
_async_session_factory = async_sessionmaker(
    bind=_engine,
    expire_on_commit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """Создает таблицы в начале тестовой сессии и удаляет в конце."""
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _engine.dispose()


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Создает сессию для теста с очисткой данных после каждого теста."""
    async with _async_session_factory() as session:
        app.dependency_overrides[get_session] = lambda: session
        yield session
        app.dependency_overrides.clear()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


@pytest.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Создает тестовый HTTP клиент."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
