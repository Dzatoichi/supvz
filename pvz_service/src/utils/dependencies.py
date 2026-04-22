from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.employeesDAO import EmployeesDAO
from src.dao.inboxDAO import InboxEventsDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.database.base import db_helper
from src.policies.employee_policy import EmployeeAccessPolicy
from src.policies.pvz_group_policy import PVZGroupAccessPolicy
from src.policies.pvz_policy import PVZAccessPolicy
from src.schemas.employees_schemas import InternalUserSchema
from src.services.employees_service import EmployeesService
from src.services.inbox_service import InboxService
from src.services.pvz_groups_service import PVZGroupsService
from src.services.pvz_service import PVZService
from src.settings.config import settings
from src.utils.exceptions import InvalidInternalApiKeyException


async def get_session() -> AsyncSession:
    async with db_helper.async_session_maker() as session:
        yield session


# DAO


def get_employees_repo(
    session: AsyncSession = Depends(get_session),
) -> EmployeesDAO:
    return EmployeesDAO(session=session)


def get_pvz_repo(
    session: AsyncSession = Depends(get_session),
) -> PVZsDAO:
    return PVZsDAO(session=session)


def get_pvz_groups_repo(
    session: AsyncSession = Depends(get_session),
) -> PVZGroupsDAO:
    return PVZGroupsDAO(session=session)


def get_inbox_repo(
    session: AsyncSession = Depends(get_session),
) -> InboxEventsDAO:
    return InboxEventsDAO(session=session)


# Policies


def get_pvz_group_policy(
    repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    return PVZGroupAccessPolicy(repo=repo)


def get_pvz_policy(
    repo: PVZsDAO = Depends(get_pvz_repo),
):
    return PVZAccessPolicy(repo=repo)


def get_employee_policy(
    repo: EmployeesDAO = Depends(get_employees_repo),
):
    return EmployeeAccessPolicy(repo=repo)


# Сервисы


def get_employees_service(
    employees_repo: EmployeesDAO = Depends(get_employees_repo),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
    employee_policy: EmployeeAccessPolicy = Depends(get_employee_policy),
    pvz_policy: PVZAccessPolicy = Depends(get_pvz_policy),
) -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService(
        employee_policy=employee_policy,
        pvz_policy=pvz_policy,
        employees_repo=employees_repo,
        pvz_repo=pvz_repo,
    )


def get_pvz_service(
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_groups_repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
    pvz_policy: PVZAccessPolicy = Depends(get_pvz_policy),
    employee_repo: EmployeesDAO = Depends(get_employees_repo),
) -> "PVZService":
    """Создает сервис для работы с пользователями."""
    return PVZService(
        pvz_repo=pvz_repo,
        pvz_groups_repo=pvz_groups_repo,
        pvz_policy=pvz_policy,
        employees_repo=employee_repo,
    )


def get_pvz_groups_service(
    group_policy: PVZGroupAccessPolicy = Depends(get_pvz_group_policy),
    group_repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
    pvz_repo: PVZsDAO = Depends(get_pvz_repo),
    employee_repo: EmployeesDAO = Depends(get_employees_repo),
) -> PVZGroupsService:
    """Создает сервис для работы с группами"""

    return PVZGroupsService(
        group_policy=group_policy,
        group_repo=group_repo,
        pvz_repo=pvz_repo,
        employee_repo=employee_repo,
    )


def get_inbox_service(
    inbox_repo: InboxEventsDAO = Depends(get_inbox_repo),
):
    return InboxService(inbox_repo=inbox_repo)


# AUTH


async def verify_internal_request(
    x_api_key: str = Header(..., alias="X-Internal-API-Key"),
) -> None:
    """Проверяет что запрос от доверенного сервиса."""

    if x_api_key != settings.INTERNAL_API_KEY:
        raise InvalidInternalApiKeyException("Недопустимый внутренний ключ API")


async def get_current_user(
    _: None = Depends(verify_internal_request),
    x_user_id: int = Header(..., alias="X-User-ID"),
) -> InternalUserSchema:
    """
    Получает user_id из заголовка, предварительно проверив API key.
    """

    return InternalUserSchema(id=x_user_id)


CurrentUserDep = Annotated[InternalUserSchema, Depends(get_current_user)]
InternalKeyDep = Depends(verify_internal_request)
IdempotencyKeyDep = Annotated[str, Header(alias="X-Idempotency-Key")]
