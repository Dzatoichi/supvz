from sqlalchemy import select

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
