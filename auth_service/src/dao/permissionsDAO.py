from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.permissions.permissions import Permissions
from src.models.position_permissions.position_permissions import PositionPermissions
from src.models.user_permissions.user_permissions import UserPermissions


class PermissionsDAO(BaseDAO[Permissions]):
    """
    Класс DAO для работы с сущностями Permission.
    """

    def __init__(self):
        super().__init__(model=Permissions)

    @BaseDAO.with_exception
    async def get_permissions(
        self,
        params: Params,
    ) -> Page[Permissions]:
        """
        Получает список прав с пагинацией.
        """
        async with self._get_session() as session:
            stmt = select(self.model)

            stmt = stmt.order_by(self.model.id.desc())

            return await paginate(session, stmt, params)

    @BaseDAO.with_exception
    async def get_permissions_ids_by_position(self, position_id: int) -> list[int]:
        """
        Возвращает список ID прав (permission_id) для указанной должности
        """
        async with self._get_session() as session:
            stmt = select(PositionPermissions.permission_id).where(PositionPermissions.position_id == position_id)

            result = await session.execute(stmt)
            return result.scalars().all()

    @BaseDAO.with_exception
    async def get_permissions_by_position(self, position_id: int, params: Params) -> Page[Permissions]:
        """Возвращает права доступа для конкретной должности"""
        async with self._get_session() as session:
            stmt = (
                select(self.model)
                .join(PositionPermissions, Permissions.id == PositionPermissions.permission_id)
                .where(PositionPermissions.position_id == position_id)
            )
            return await paginate(session, stmt, params)

    @BaseDAO.with_exception
    async def add_permissions_to_position(
        self,
        position_id: int,
        permission_ids: list[int],
        session: AsyncSession,
    ) -> None:
        """
        Массовая вставка связей в таблицу ассоциации.
        """

        # Формируем список словарей для вставки
        stmt = insert(PositionPermissions).values(
            [{"position_id": position_id, "permission_id": p_id} for p_id in permission_ids]
        )

        await session.execute(stmt)

    @BaseDAO.with_exception
    async def set_permissions_for_position(
        self,
        position_id: int,
        new_permission_ids: list[int],
        session: AsyncSession,
    ) -> None:
        """Полностью обновляет права должности: удаляет все старые и вставляет новые."""

        await session.execute(delete(PositionPermissions).where(PositionPermissions.position_id == position_id))

        if not new_permission_ids:
            return

        stmt = insert(PositionPermissions).values(
            [{"position_id": position_id, "permission_id": p} for p in new_permission_ids]
        )
        await session.execute(stmt)

    async def get_permissions_by_user(self, user_id: int, params: Params) -> Page[Permissions]:
        """Метод получения прав пользователя"""

        async with self._get_session() as session:
            stmt = select(Permissions).join(UserPermissions).where(UserPermissions.user_id == user_id)
            return await paginate(session, stmt, params)

    @BaseDAO.with_exception
    async def get_user_permissions_without_pagination(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[Permissions]:
        """
        Возвращает список объектов Permissions, привязанных к юзеру.
        """
        stmt = (
            select(Permissions)
            .join(UserPermissions, Permissions.id == UserPermissions.permission_id)
            .where(UserPermissions.user_id == user_id)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
