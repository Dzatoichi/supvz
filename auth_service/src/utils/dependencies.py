from src.dao.tokensDAO import StatefulTokenDAO
from src.dao.usersDAO import UsersDAO
from src.services.token_service import JWTTokensService, StatefulTokenService
from src.services.user_service import UserService


def get_users_dao() -> UsersDAO:
    """Создаёт репозиторий (сессия внутри через _get_session)."""
    return UsersDAO()


def get_token_dao() -> StatefulTokenDAO:
    """Создаём DAO для работы с stateful токенами."""
    return StatefulTokenDAO()


def get_stateful_token_service() -> StatefulTokenService:
    """Создает сервис для работы с stateful токенами."""
    return StatefulTokenService()


def get_auth_service() -> "AuthService":  # type: ignore # noqa: F821
    """Создаёт сервис для работы с авторизацией."""
    from src.services.auth_service import AuthService

    return AuthService()


def get_user_service() -> "UserService":
    """Создает сервис для работы с пользователями."""
    return UserService()


def get_jwt_tokens_service() -> JWTTokensService:
    """Создаёт сервис для работы с JWT токенами."""
    return JWTTokensService()
