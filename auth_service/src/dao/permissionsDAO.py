from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.permissions.permissions import Permissions
from src.models.positions.positions import PositionPermissions


class PermissionsDAO(BaseDAO[Permissions]):
    """
    Класс DAO для работы с сущностями Permission.
    """

    def __init__(self):
        super().__init__(model=Permissions)

    @BaseDAO.with_exception
    async def get_permissions_by_position(self, position_id: int) -> list[Permissions]:
        """
        Получение всех permissions, связанных с конкретной должностью (position_id).
        """
        async with self._get_session() as session:
            stmt = (
                select(self.model)
                .join(
                    PositionPermissions,
                    self.model.id == PositionPermissions.permission_id,
                )
                .where(PositionPermissions.position_id == position_id)
            )
            res = await session.execute(stmt)
            return res.scalars().all()

    @BaseDAO.with_exception
    async def add_permissions_to_position(
        self,
        position_id: int,
        permission_ids: list[int],
        session: AsyncSession,
    ):
        """
        Массовая вставка связей в таблицу ассоциации.
        """
        if not permission_ids:
            return

        # Формируем список словарей для вставки
        stmt = insert(PositionPermissions).values(
            [{"position_id": position_id, "permission_id": p_id} for p_id in permission_ids]
        )

        await session.execute(stmt)

    @BaseDAO.with_exception
    async def get_by_ids(
        self,
        permission_ids: list[int],
        session: AsyncSession,
    ) -> list[Permissions]:
        if not permission_ids:
            return []

        query = select(self.model).where(self.model.id.in_(permission_ids))
        result = await session.execute(query)
        return result.scalars().all()
