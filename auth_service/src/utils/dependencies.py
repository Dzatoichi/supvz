from fastapi import Depends

from auth_service.src.dao.usersDAO import UsersDAO
from auth_service.src.database.base import db_helper
from auth_service.src.services.auth_service import AuthService
from auth_service.src.services.token_service import JWTTokensService, StatefulTokenService


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


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


def get_users_dao() -> UsersDAO:
    """Создаёт репозиторий (сессия внутри через _get_session)."""
    return UsersDAO()


def get_token_service() -> StatefulTokenService:
    """Создаёт сервис с созданием/проверкой токена JWT."""
    return StatefulTokenService()


def get_auth_service_without_token(
        repo: UsersDAO = Depends(get_users_dao)
) -> AuthService:
    """Создаёт сервис с репозиторием без токена."""
    return AuthService(repo)


def get_auth_service_with_token(
        repo: UsersDAO = Depends(get_users_dao),
        token_service: StatefulTokenService = Depends(get_token_service)
) -> AuthService:
    """Создаёт сервис с репозиторием и токеном."""
    return AuthService(repo, token_service)
