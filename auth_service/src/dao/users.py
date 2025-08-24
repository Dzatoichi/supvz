from auth_service.src.dao.base import BaseDAO
from auth_service.src.models.users.users import Users


class UsersDAO(BaseDAO[Users]):
    def __init__(self):
        super().__init__(model=Users)