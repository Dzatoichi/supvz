from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.dao.baseDAO import BaseDAO
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
    async def assign_permissions(self, user_id: int, permissions: list, session: AsyncSession) -> None:
        """Назначает пользователю список permissions"""
        for perm in permissions:
            user_perm = UserPermissions(user_id=user_id, permission_id=perm.id)
            session.add(user_perm)

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
