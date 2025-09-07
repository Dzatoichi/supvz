from fastapi import Depends

from src.dao.tokensDAO import StatefulTokenDAO
from src.dao.usersDAO import UsersDAO
from src.services.auth_service import AuthService
from src.services.token_service import StatefulTokenService


def get_users_dao() -> UsersDAO:
    """Создаёт репозиторий (сессия внутри через _get_session)."""
    return UsersDAO()


def get_token_dao() -> StatefulTokenDAO:
    """Создаём DAO для работы с stateful токенами."""
    return StatefulTokenDAO()


def get_stateful_token_service(
        dao: StatefulTokenDAO = Depends(get_token_dao)  # noqa: B008
) -> StatefulTokenService:
    """Создает сервис для работы с stateful токенами."""
    return StatefulTokenService(dao)


def get_auth_service_without_token(
        repo: UsersDAO = Depends(get_users_dao)  # noqa: B008
) -> AuthService:
    """Создаёт сервис с репозиторием без токена."""
    return AuthService(repo)


def get_auth_service_with_token(
        repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
        token_service: StatefulTokenService = Depends(get_stateful_token_service)  # noqa: B008
) -> AuthService:
    """Создаёт сервис с репозиторием и токеном."""
    return AuthService(repo, token_service)
