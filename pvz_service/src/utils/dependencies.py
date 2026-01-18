from typing import Annotated

from fastapi import Depends, Header

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.database.base import db_helper
from src.schemas.employees_schemas import InternalUserSchema
from src.services.employees_service import EmployeesService
from src.services.pvz_groups_service import PVZGroupsService
from src.services.pvz_service import PVZService
from src.settings.config import settings
from src.utils.exceptions import InvalidInternalApiKeyException

# DAO


def get_employees_repo() -> EmployeesDAO:
    return EmployeesDAO()


def get_pvz_repo() -> PVZsDAO:
    return PVZsDAO()


def get_pvz_groups_repo() -> PVZGroupsDAO:
    return PVZGroupsDAO()


# Сервисы


def get_employees_service() -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService()


def get_pvz_service() -> "PVZService":
    """Создает сервис для работы с пользователями."""
    return PVZService()


def get_pvz_groups_service() -> PVZGroupsService:
    """Создает сервис для работы с группами"""
    return PVZGroupsService(db_helper=db_helper)


# AUTH


async def verify_internal_request(
    x_api_key: str = Header(..., alias="X-Internal-API-Key"),
) -> None:
    """Проверяет что запрос от доверенного сервиса."""

    if x_api_key != settings.INTERNAL_API_KEY:
        raise InvalidInternalApiKeyException("Invalid internal API key")


async def get_current_user(
    _: None = Depends(verify_internal_request),
    x_user_id: int = Header(..., alias="X-User-ID"),
) -> InternalUserSchema:
    """
    Получает user_id из заголовка, предварительно проверив API key.
    """

    return InternalUserSchema(id=x_user_id)


CurrentUserDep = Annotated[InternalUserSchema, Depends(get_current_user)]
