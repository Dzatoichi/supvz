from fastapi import Depends, HTTPException, Request, status

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.positionsDAO import PositionDAO
from src.dao.tokensDAO import RefreshTokensDAO, StatefulTokenDAO
from src.dao.usersDAO import UsersDAO
from src.database.base import db_helper
from src.schemas.users_schemas import UserAuthRequestSchema
from src.services.permission_service import PermissionService
from src.services.position_service import PositionService
from src.services.token_service import JWTTokensService, StatefulTokenService
from src.services.user_service import UserService

# region DAOS


def get_users_dao() -> UsersDAO:
    """Создаёт репозиторий (сессия внутри через _get_session)."""
    return UsersDAO()


def get_stateful_token_dao() -> StatefulTokenDAO:
    """Создаём DAO для работы с stateful токенами."""
    return StatefulTokenDAO()


def get_refresh_token_dao() -> RefreshTokensDAO:
    """Создаём DAO для работы с refresh токенами"""
    return RefreshTokensDAO()


def get_permissions_dao() -> PermissionsDAO:
    """Создаем DAO для работы с Permissions."""
    return PermissionsDAO()


def get_position_dao() -> PositionDAO:
    """Создаем DAO для работы с Position."""
    return PositionDAO()


# region Сервисы


def get_stateful_token_service(
    dao: StatefulTokenDAO = Depends(get_stateful_token_dao),
) -> StatefulTokenService:
    """Создает сервис для работы с stateful токенами."""
    return StatefulTokenService(dao=dao)


def get_auth_service() -> "AuthService":  # type: ignore
    """Создаёт сервис для работы с авторизацией."""
    from src.services.auth_service import AuthService

    return AuthService(db_helper=db_helper)


def get_user_service() -> "UserService":
    """Создает сервис для работы с пользователями."""
    return UserService(db_helper=db_helper)


def get_jwt_tokens_service(
    repo: RefreshTokensDAO = Depends(get_refresh_token_dao),
) -> JWTTokensService:
    """Создаёт сервис для работы с JWT токенами."""

    return JWTTokensService(repo=repo)


def get_position_service(
    position_dao: PositionDAO = Depends(get_position_dao),
    permissions_dao: PermissionsDAO = Depends(get_permissions_dao),
) -> "PositionService":
    """Создает сервис для работы с должностями."""
    return PositionService(
        db_helper=db_helper,
        position_dao=position_dao,
        permissions_dao=permissions_dao,
    )


def get_permissions_service(
    permissions_dao: PermissionsDAO = Depends(get_permissions_dao),
) -> "PermissionService":
    """Создает сервис для работы с правами доступа"""
    return PermissionService(permissions_dao=permissions_dao)


def get_access_token_from_cookie(request: Request) -> UserAuthRequestSchema:
    """Зависимость для получения access токена из куки"""
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found in cookies",
        )
    return access_token
