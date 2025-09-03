from auth_service.src.dao.usersDAO import UsersDAO
from auth_service.src.services.auth_service import AuthService
from auth_service.src.services.token_service import StatefulTokenService
from fastapi import Depends


def get_users_dao() -> UsersDAO:
    """Создаёт репозиторий (сессия внутри через _get_session)."""
    return UsersDAO()


def get_token_service() -> StatefulTokenService:
    """Создаёт сервис с созданием/проверкой токена JWT."""
    return StatefulTokenService()


def get_auth_service_without_token(
        repo: UsersDAO = Depends(get_users_dao)  # noqa: B008
) -> AuthService:
    """Создаёт сервис с репозиторием без токена."""
    return AuthService(repo)


def get_auth_service_with_token(
        repo: UsersDAO = Depends(get_users_dao),  # noqa: B008
        token_service: StatefulTokenService = Depends(get_token_service)  # noqa: B008
) -> AuthService:
    """Создаёт сервис с репозиторием и токеном."""
    return AuthService(repo, token_service)
