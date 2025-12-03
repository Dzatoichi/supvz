from pydantic import EmailStr
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.dao.baseDAO import BaseDAO
from src.models import Permissions
from src.models.user_permissions.user_permissions import UserPermissions
from src.models.users.users import Users


class UsersDAO(BaseDAO[Users]):
    """
    Класс, наследующий базовый DAO для работы с сущностями пользователя.
    """

    def __init__(self):
        super().__init__(model=Users)

    @BaseDAO.with_exception
    async def get_user_by_email(self, email: EmailStr) -> Users | None:
        """
        Метод получения пользователя по email.
        """
        async with self._get_session() as session:
            stmt = select(self.model).where(self.model.email == email)
            res = await session.execute(stmt)
            return res.scalars().first()

    @BaseDAO.with_exception
    async def set_password(self, user_id: int, hashed_password: str) -> bool:
        """
        Метод изменения пароля.
        """
        updated_user = await self.update(id=user_id, hashed_password=hashed_password)
        if not updated_user:
            raise NoResultFound(f"Пользователь с id={user_id} не найден")
        return True

    @BaseDAO.with_exception
    async def assign_permissions(self, user_id: int, permissions: list[int], session: AsyncSession) -> None:
        """Назначает пользователю список permissions"""
        stmt = insert(UserPermissions).values([{"user_id": user_id, "permission_id": p_id} for p_id in permissions])
        await session.execute(stmt)

    @BaseDAO.with_exception
    async def create_user(self, payload: dict, session: AsyncSession) -> Users:
        """Метод создания пользователя"""
        user = Users(**payload)
        session.add(user)
        await session.flush()
        return user

    @BaseDAO.with_exception
    async def get_user_with_permissions(self, user_id: int, session: AsyncSession):
        """Метод получения пользователя с permissions"""
        query = (
            select(self.model)
            .options(selectinload(self.model.permission_links).selectinload(UserPermissions.permission))
            .where(self.model.id == user_id)
        )
        result = await session.execute(query)
        return result.scalar_one()

    @BaseDAO.with_exception
    async def get_user_permissions(self, session: AsyncSession, user_id: int) -> list[Permissions]:
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

    @BaseDAO.with_exception
    async def update_user_permissions(self, session: AsyncSession, user_id: int, new_permission_ids: list[int]) -> None:
        """Обновляет права пользователя"""

        # Получаем текущие ID прав
        stmt = select(UserPermissions.permission_id).where(UserPermissions.user_id == user_id)
        result = await session.execute(stmt)
        current_ids = set(result.scalars().all())

        target_ids = set(new_permission_ids)

        # Вычисляем разницу
        to_delete = current_ids - target_ids
        to_add = target_ids - current_ids

        # Удаляем те, которых нет в новом списке
        if to_delete:
            await session.execute(
                delete(UserPermissions).where(
                    UserPermissions.user_id == user_id,
                    UserPermissions.permission_id.in_(to_delete),
                )
            )

        # Добавляем новые
        if to_add:
            await session.execute(
                insert(UserPermissions).values([{"user_id": user_id, "permission_id": p_id} for p_id in to_add])
            )
