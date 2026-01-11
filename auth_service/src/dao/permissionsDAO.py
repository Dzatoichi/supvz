from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.permissions.permissions import Permissions
from src.models.position_permissions.custom_position_permissions import CustomPositionPermissions
from src.models.position_permissions.system_position_permissions import (
    SystemPositionPermissions,
)
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

            return await apaginate(session, stmt, params)

    @BaseDAO.with_exception
    async def get_permissions_ids_by_system_position(self, position_id: int) -> list[int]:
        """
        Возвращает список ID прав (permission_id) из системной должности.
        """
        async with self._get_session() as session:
            stmt = select(SystemPositionPermissions.permission_id).where(
                SystemPositionPermissions.system_position_id == position_id
            )

            result = await session.execute(stmt)
            return result.scalars().all()

    @BaseDAO.with_exception
    async def get_permissions_ids_by_custom_position(self, position_id: int) -> list[int]:
        """
        Возвращает список ID прав (permission_id) из кастомной должности.
        """
        async with self._get_session() as session:
            stmt = select(CustomPositionPermissions.permission_id).where(
                CustomPositionPermissions.custom_position_id == position_id
            )

            result = await session.execute(stmt)
            return result.scalars().all()

    @BaseDAO.with_exception
    async def get_permissions_by_system_position(self, position_id: int, params: Params) -> Page[Permissions]:
        """Возвращает права доступа для конкретной должности"""
        async with self._get_session() as session:
            stmt = (
                select(self.model)
                .join(SystemPositionPermissions, Permissions.id == SystemPositionPermissions.permission_id)
                .where(SystemPositionPermissions.system_position_id == position_id)
            )
            return await apaginate(session, stmt, params)

    @BaseDAO.with_exception
    async def get_permissions_by_custom_position(self, position_id: int, params: Params) -> Page[Permissions]:
        """Возвращает права доступа для конкретной должности"""
        async with self._get_session() as session:
            stmt = (
                select(self.model)
                .join(CustomPositionPermissions, Permissions.id == CustomPositionPermissions.permission_id)
                .where(CustomPositionPermissions.custom_position_id == position_id)
            )
            return await apaginate(session, stmt, params)

    @BaseDAO.with_exception
    async def add_permissions_to_custom_position(
        self,
        position_id: int,
        permission_ids: list[int],
        session: AsyncSession,
    ) -> None:
        """
        Массовая вставка связей в таблицу ассоциации
        """

        # Формируем список словарей для вставки
        stmt = insert(CustomPositionPermissions).values(
            [{"custom_position_id": position_id, "permission_id": p_id} for p_id in permission_ids]
        )

        await session.execute(stmt)

    @BaseDAO.with_exception
    async def set_permissions_for_custom_position(
        self,
        position_id: int,
        new_permission_ids: list[int],
        session: AsyncSession,
    ) -> list[int]:
        """Полностью обновляет права должности: удаляет все старые и вставляет новые."""

        await session.execute(
            delete(CustomPositionPermissions).where(CustomPositionPermissions.custom_position_id == position_id)
        )

        stmt = insert(CustomPositionPermissions).values(
            [{"custom_position_id": position_id, "permission_id": p} for p in new_permission_ids]
        )
        await session.execute(stmt)

        return new_permission_ids

    async def get_permissions_by_user(self, user_id: int, params: Params) -> Page[Permissions]:
        """Метод получения прав пользователя"""

        async with self._get_session() as session:
            stmt = select(Permissions).join(UserPermissions).where(UserPermissions.user_id == user_id)
            return await apaginate(session, stmt, params)

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
