from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from src.core.security.hash_helper import HashHelper
from src.dao.baseDAO import BaseDAO
from src.models.users.users import Users


class UsersDAO(BaseDAO[Users]):
    def __init__(self):
        super().__init__(model=Users)

    async def get_user_by_email(self, email: str) -> Users:
        try:
            async with self._get_session() as session:
                stmt = select(self.model).where(self.model.email == email)
                res = await session.execute(stmt)
                result = res.scalars().first()

                if not result:
                    raise NoResultFound(f"Пользователь с почтой: {email} не найден")

                return result
        except SQLAlchemyError as e:
            raise e

    async def set_password(self, user_id: int, new_password: str):
        """Обновление пароля пользователя."""
        try:
            hashed_password = HashHelper.hash(new_password)

            updated_user = await self.update(user_id, password=hashed_password)

            if not updated_user:
                raise NoResultFound(f"Пользователь с id={user_id} не найден")

            return {"detail": "Password reset successful"}

        except SQLAlchemyError as e:
            raise e
