from fastapi_pagination import Page, Params

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.positionsDAO import CustomPositionDAO, SystemPositionDAO
from src.schemas.positions_schemas import (
    CustomPositionCreateSchema,
    CustomPositionUpdateSchema,
    CustomPositionWithPermissionsReadSchema,
    PositionReadSchema,
    PositionSourceEnum,
)
from src.utils.exceptions import (
    PositionAlreadyExistsException,
    PositionNotFoundException,
)


class PositionService:
    """Сервис для работы с должностями"""

    def __init__(
        self,
        db_helper,
        custom_position_dao: CustomPositionDAO,
        system_position_dao: SystemPositionDAO,
        permissions_dao: PermissionsDAO,
    ):
        self.db_helper = db_helper
        self.custom_position_dao = custom_position_dao
        self.system_position_dao = system_position_dao
        self.perm_dao = permissions_dao

    async def get_positions(
        self,
        params: Params,
        position_source: PositionSourceEnum,
        owner_id: int | None = None,
    ) -> Page[PositionReadSchema]:
        """Возвращает список всех должностей с возможностью отфильтровать по owner_id"""

        if position_source == PositionSourceEnum.system:
            positions = await self.system_position_dao.get_positions(params=params)
        elif position_source == PositionSourceEnum.custom:
            positions = await self.custom_position_dao.get_positions(owner_id=owner_id, params=params)

        if positions.total == 0:
            raise PositionNotFoundException("Не найдено ни одной должности.")

        positions.items = [PositionReadSchema.model_validate(pos) for pos in positions.items]
        return positions

    async def get_position(
        self,
        position_id: int,
        position_source: PositionSourceEnum,
    ) -> PositionReadSchema:
        """Возвращает одну должность по id"""

        if position_source == PositionSourceEnum.system:
            position = await self.system_position_dao.get_by_id(id=position_id)
        elif position_source == PositionSourceEnum.custom:
            position = await self.custom_position_dao.get_by_id(id=position_id)

        if not position:
            raise PositionNotFoundException("Должность с таким id не найдена.")

        return PositionReadSchema.model_validate(position)

    async def create_position(
        self,
        data: CustomPositionCreateSchema,
    ) -> PositionReadSchema:
        """Создает новую кастомную должность"""

        payload = {
            "title": data.title,
            "owner_id": data.owner_id,
        }

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                position = await self.custom_position_dao.get_position(
                    title=data.title,
                    owner_id=data.owner_id,
                    session=session,
                )

                if position:
                    raise PositionAlreadyExistsException("Должность с таким именем уже существует.")

                position = await self.custom_position_dao.create(
                    payload=payload,
                    session=session,
                )

                if data.permissions:
                    await self.perm_dao.add_permissions_to_custom_position(
                        position_id=position.id,
                        permission_ids=data.permissions,
                        session=session,
                    )

                else:
                    position.permissions = None

                return PositionReadSchema.model_validate(position)

    async def update_position(
        self,
        position_id: int,
        data: CustomPositionUpdateSchema,
    ) -> CustomPositionWithPermissionsReadSchema:
        """Обновляет имя и права долджности"""

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                existing_position = await self.custom_position_dao.get_position(
                    id=position_id,
                    session=session,
                )
                if not existing_position:
                    raise PositionNotFoundException("Должность с таким id не найдена.")

                current_position = existing_position

                if data.title:
                    current_position = await self.custom_position_dao.update(
                        position_id=position_id,
                        title=data.title,
                        session=session,
                    )

                if data.permissions_ids is not None:
                    final_permission_ids = await self.perm_dao.set_permissions_for_custom_position(
                        position_id=position_id,
                        new_permission_ids=data.permissions_ids,
                        session=session,
                    )
                else:
                    final_permission_ids = await self.perm_dao.get_permissions_ids_by_custom_position(
                        position_id=position_id,
                    )

                return CustomPositionWithPermissionsReadSchema(
                    id=current_position.id,
                    owner_id=current_position.owner_id,
                    title=current_position.title,
                    permissions_ids=final_permission_ids,
                )

    async def delete_position(self, position_id: int) -> None:
        """Метод удалаяет должность по id"""

        await self.custom_position_dao.delete(id=position_id)
