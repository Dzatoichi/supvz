from fastapi_pagination import Page, Params
from pydantic import TypeAdapter

from src.dao.permissionsDAO import PermissionsDAO
from src.schemas.enums import PositionSourceEnum
from src.schemas.permissions_schemas import PermissionReadSchema
from src.utils.exceptions import PermissionsFilterException, PermissionsNotFound


class PermissionService:
    """Сервис для работы с правами доступа"""

    def __init__(self, permissions_dao: PermissionsDAO):
        self.perm_dao = permissions_dao
        self.permission_adapter = TypeAdapter(PermissionReadSchema)

    async def get_permissions_filtered(
        self,
        position_id: int | None,
        position_source: PositionSourceEnum | None,
        user_id: int | None,
        params: Params,
    ) -> Page[PermissionReadSchema]:
        """Получение прав доступа с пагинацией и фильтрацией."""

        if position_id is not None and user_id is not None:
            raise PermissionsFilterException("Нужно передавать либо position_id, либо user_id, но не оба.")

        perms = None

        if position_id is not None:
            if position_source is None:
                raise PermissionsFilterException("При фильтрации по position_id обязательно указывать position_source.")

            if position_source == PositionSourceEnum.system:
                perms = await self.perm_dao.get_permissions_by_system_position(
                    position_id=position_id,
                    params=params,
                )
            elif position_source == PositionSourceEnum.custom:
                perms = await self.perm_dao.get_permissions_by_custom_position(
                    position_id=position_id,
                    params=params,
                )

        elif user_id is not None:
            perms = await self.perm_dao.get_permissions_by_user(user_id=user_id, params=params)

        else:
            perms = await self.perm_dao.get_permissions(params=params)

        if perms.total == 0:
            raise PermissionsNotFound("Никаких прав доступа не найдено.")

        perms.items = [self.permission_adapter.validate_python(perm) for perm in perms.items]

        return perms
