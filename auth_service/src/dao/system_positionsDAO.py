from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select

from src.dao.baseDAO import BaseDAO
from src.models import SystemPositions


class SystemPositionDAO(BaseDAO[SystemPositions]):
    """
    Класс DAO для работы с сущностями SystemPositions.
    """

    def __init__(self):
        super().__init__(model=SystemPositions)

    @BaseDAO.with_exception
    async def get_positions(
        self,
        params: Params,
    ) -> Page[SystemPositions]:
        """
        Получает список должностей с фильтрацией и пагинацией.
        """
        async with self._get_session() as session:
            stmt = select(self.model).order_by(self.model.id.desc())

            return await apaginate(session, stmt, params)
