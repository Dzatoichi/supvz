from src.dao.permissionsDAO import PermissionsDAO
from src.schemas.perm_positions_schemas import PermissionReadSchema
from src.utils.exceptions import PermissionsFilterException, PermissionsNotFound


class PermissionService:
    """Сервис для работы с правами доступа"""

    async def get_permissions(self, repo: PermissionsDAO) -> list[PermissionReadSchema]:
        permissions = await repo.get_all()

        if permissions is None:
            raise PermissionsNotFound("Никаких прав доступа не найдено.")

        return [PermissionReadSchema.model_validate(perm) for perm in permissions]

    async def get_permissions_filtered(
        self,
        position_id: int | None,
        user_id: int | None,
        repo: PermissionsDAO,
    ) -> list[PermissionReadSchema]:
        """Получение прав доступа. Проверяет, что передан ровно один фильтр."""

        if position_id is None and user_id is None:
            perms = await repo.get_all()

        elif position_id is not None and user_id is not None:
            raise PermissionsFilterException("Нужно передавать либо position_id, либо user_id, но не оба.")

        elif position_id is not None:
            perms = await repo.get_permissions_by_position(position_id=position_id)

        else:
            perms = await repo.get_permissions_by_user(user_id=user_id)

        if not perms:
            raise PermissionsNotFound("Никаких прав доступа не найдено.")

        return [PermissionReadSchema.model_validate(p) for p in perms]
