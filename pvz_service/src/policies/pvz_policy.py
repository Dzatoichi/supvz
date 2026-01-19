from src.dao.pvzsDAO import PVZsDAO
from src.utils.exceptions import AccessDeniedException, PVZNotFoundException


class PVZAccessPolicy:
    def __init__(self, repo: PVZsDAO):
        self.repo = repo

    async def check_owner_or_responsible(
        self,
        pvz_id: int,
        current_user_id: int,
    ) -> None:
        """Проверяет, является ли пользователь владельцем или ответственным за ПВЗ."""
        pvz = await self.repo.get_pvz(id=pvz_id)
        if not pvz:
            raise PVZNotFoundException("ПВЗ не найден")

        if pvz.owner_id != current_user_id and getattr(pvz, "responsible_id", None) != current_user_id:
            raise AccessDeniedException("Нет доступа к данному ПВЗ")

    async def check_pvz_access(
        self,
        pvz_id: int,
        current_user_id: int,
    ) -> None:
        """Универсальная проверка доступа к ПВЗ."""
        await self.check_owner_or_responsible(pvz_id, current_user_id)
