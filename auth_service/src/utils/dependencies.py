from fastapi import Depends

from .service import AuthService, TokenService


class FakeAuthRepository:
    pass


class FakeAsyncSession:
    pass


async def get_async_session() -> FakeAsyncSession:
    """Создаёт и управляет сессией БД для одного запроса."""

    # async with async_session_maker() as session:
    #     yield session
    pass


async def get_auth_repo(
        session: FakeAsyncSession = Depends(get_async_session)
) -> FakeAuthRepository:
    """Создаёт репозиторий с сессией БД."""

    # return AuthRepository(session)
    pass


def get_token_service() -> TokenService:
    """Создаёт сервис с созданием/проверкой токена JWT."""
    # return TokenService()
    pass


def get_auth_service_without_token(
        repo: FakeAuthRepository = Depends(get_auth_repo)
) -> AuthService:
    """Создаёт сервис с репозиторием без токена."""

    # return AuthService(repo)
    pass


async def get_auth_service_with_token(
        repo: FakeAuthRepository = Depends(get_auth_repo),
        token_service: TokenService = Depends(get_token_service)
) -> AuthService:
    """Создаёт сервис с репозиторием и токеном."""

    # return AuthService(repo, token_service)
    pass
