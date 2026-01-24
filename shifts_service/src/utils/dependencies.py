from collections.abc import AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.shift_penaltiesDAO import PenaltiesDAO
from src.dao.shiftsDAO import ShiftsDAO
from src.database.base import db_helper
from src.services.shift_penalties_service import PenaltiesService
from src.services.shifts_service import ShiftsService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
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
    return ShiftsDAO(session=session)


def get_shift_service(
    dao: ShiftsDAO = Depends(get_shifts_dao),
) -> ShiftsService:
    return ShiftsService(dao=dao)


def get_penalties_dao(
    session: AsyncSession = Depends(get_session),
) -> PenaltiesDAO:
    return PenaltiesDAO(session=session)


def get_penalties_service(
    dao: PenaltiesDAO = Depends(get_penalties_dao),
) -> PenaltiesService:
    return PenaltiesService(dao=dao)
