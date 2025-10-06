from fastapi import Depends, HTTPException, Request, status

from src.dao.tokensDAO import RefreshTokensDAO, StatefulTokenDAO
from src.dao.usersDAO import UsersDAO
from src.services.token_service import JWTTokensService, StatefulTokenService
from src.services.user_service import UserService

# DAO


def get_users_dao() -> UsersDAO:
    """Создаёт репозиторий (сессия внутри через _get_session)."""
    return UsersDAO()


def get_stateful_token_dao() -> StatefulTokenDAO:
    """Создаём DAO для работы с stateful токенами."""
    return StatefulTokenDAO()


def get_refresh_token_dao() -> RefreshTokensDAO:
    """Создаём DAO для работы с refresh токенами"""
    return RefreshTokensDAO()


# Сервисы


def get_stateful_token_service(
    dao: StatefulTokenDAO = Depends(get_stateful_token_dao),
) -> StatefulTokenService:
    """Создает сервис для работы с stateful токенами."""
    return StatefulTokenService(dao=dao)


def get_auth_service() -> "AuthService":  # type: ignore
    """Создаёт сервис для работы с авторизацией."""
    from src.services.auth_service import AuthService

    return AuthService()


def get_user_service() -> "UserService":
    """Создает сервис для работы с пользователями."""
    return UserService()


def get_jwt_tokens_service(
    repo: RefreshTokensDAO = Depends(get_refresh_token_dao),
) -> JWTTokensService:
    """Создаёт сервис для работы с JWT токенами."""

    return JWTTokensService(repo=repo)


def get_access_token_from_cookie(request: Request) -> str:
    """Зависимость для получения access токена из куки"""
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found in cookies")
    return access_token
