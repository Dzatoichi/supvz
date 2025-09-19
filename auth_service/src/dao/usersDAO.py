from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.dao.baseDAO import BaseDAO
from src.models.users.users import Users


class UsersDAO(BaseDAO[Users]):
    def __init__(self):
        super().__init__(model=Users)

    @BaseDAO.with_exception
    async def get_user_by_email(self, email: str) -> Users | None:
        async with self._get_session() as session:
            stmt = select(self.model).where(self.model.email == email)
            res = await session.execute(stmt)
            return res.scalars().first()

    @BaseDAO.with_exception
    async def set_password(self, user_id: int, hashed_password: str) -> bool:
        updated_user = await self.update(user_id, password=hashed_password)
        if not updated_user:
            raise NoResultFound(f"Пользователь с id={user_id} не найден")
        return True
