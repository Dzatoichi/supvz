from abc import ABC, abstractmethod


class FakeAbstractRepository(ABC):
    @abstractmethod
    def get_by_email(self, email):
        # return user_db.one_or_none(email=email)
        pass

    async def set_password(self, id, new_password):
        pass
