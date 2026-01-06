from collections.abc import AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.shiftsDAO import ShiftsDAO
from src.database.base import db_helper
from src.services.shift_service import ShiftService


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
) -> ShiftService:
    return ShiftService(dao=dao)
