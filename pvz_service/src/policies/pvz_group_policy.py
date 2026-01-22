from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.utils.exceptions import AccessDeniedException, PVZGroupNotFoundException


class PVZGroupAccessPolicy:
    def __init__(self, repo: PVZGroupsDAO):
        self.repo = repo

    async def check_group_access(
        self,
        group_id: int,
        current_user_id: int,
    ) -> None:
        """
        Проверяет, является ли пользователь владельцем или куратором группы.
        Кидает исключение, если нет доступа.
        """
        group = await self.repo.get_by_id(id=group_id)

        if not group:
            raise PVZGroupNotFoundException("Группа не найдена")

        if group.owner_id != current_user_id and group.responsible_id != current_user_id:
            raise AccessDeniedException("Нет доступа к группе ПВЗ")
