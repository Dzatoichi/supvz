from collections.abc import AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.salary_rulesDAO import SalaryRuleDAO
from src.dao.shift_penaltiesDAO import PenaltiesDAO
from src.dao.shift_requestsDAO import ShiftRequestsDAO
from src.dao.shiftsDAO import ShiftsDAO
from src.database.base import db_helper
from src.services.salary_rules_service import SalaryRulesService
from src.services.shift_penalties_service import PenaltiesService
from src.services.shift_requests_service import ShiftRequestsService
from src.services.shifts_service import ShiftsService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии БД."""
    async with db_helper.async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_shifts_dao(
    session: AsyncSession = Depends(get_session),
) -> ShiftsDAO:
    """Получение ShiftsDAO."""
    return ShiftsDAO(session=session)


def get_shift_service(
    dao: ShiftsDAO = Depends(get_shifts_dao),
) -> ShiftsService:
    """Получение ShiftsService."""
    return ShiftsService(dao=dao)


def get_penalties_dao(
    session: AsyncSession = Depends(get_session),
) -> PenaltiesDAO:
    """Получение PenaltiesDAO."""
    return PenaltiesDAO(session=session)


def get_penalties_service(
    dao: PenaltiesDAO = Depends(get_penalties_dao),
) -> PenaltiesService:
    """Получение PenaltiesService."""
    return PenaltiesService(dao=dao)


def get_shift_requests_dao(
    session: AsyncSession = Depends(get_session),
) -> ShiftRequestsDAO:
    """Получение ShiftRequestsDAO."""
    return ShiftRequestsDAO(session=session)


def get_shift_requests_service(
    dao: ShiftRequestsDAO = Depends(get_shift_requests_dao),
) -> ShiftRequestsService:
    """Получение ShiftRequestsService."""
    return ShiftRequestsService(dao=dao)


def get_salary_rule_dao(
    session: AsyncSession = Depends(get_session),
) -> SalaryRuleDAO:
    """Получение SalaryRuleDAO."""
    return SalaryRuleDAO(session=session)


def get_salary_rule_service(
    dao: SalaryRuleDAO = Depends(get_salary_rule_dao),
) -> SalaryRulesService:
    """Получение SalaryRulesService."""
    return SalaryRulesService(dao=dao)
