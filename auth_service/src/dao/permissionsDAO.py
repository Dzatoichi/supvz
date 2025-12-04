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
        Возвращает список ID прав (permission_id) для указанной должности.
        """
        async with self._get_session() as session:
            stmt = select(PositionPermissions.permission_id).where(PositionPermissions.position_id == position_id)

            result = await session.execute(stmt)
            return list(result.scalars().all())

    @BaseDAO.with_exception
    async def get_permissions_by_position(self, position_id: int, params: Params) -> Page[Permissions]:
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
    async def set_permissions_for_position(
        self,
        position_id: int,
        new_permission_ids: list[int],
        session: AsyncSession,
    ):
        """Обновляет список прав должности: удаляет лишние,
        добавляет новые, оставляет существующие"""

        # Получаем текущие права
        result = await session.execute(
            select(PositionPermissions.permission_id).where(PositionPermissions.position_id == position_id)
        )
        current_ids = {row[0] for row in result.fetchall()}

        new_ids = set(new_permission_ids)

        # Определяем какие удалить и какие добавить
        to_delete = current_ids - new_ids
        to_add = new_ids - current_ids

        # Удаляем лишние связи
        if to_delete:
            await session.execute(
                delete(PositionPermissions).where(
                    PositionPermissions.position_id == position_id,
                    PositionPermissions.permission_id.in_(to_delete),
                )
            )

        # Добавляем новые связи
        if to_add:
            stmt = insert(PositionPermissions).values(
                [{"position_id": position_id, "permission_id": p} for p in to_add]
            )
            await session.execute(stmt)

    async def get_permissions_by_user(self, user_id: int, params: Params) -> Page[Permissions]:
        """Метод получения прав пользователя"""

        async with self._get_session() as session:
            stmt = select(Permissions).join(UserPermissions).where(UserPermissions.user_id == user_id)
            return await paginate(session, stmt, params)
