from fastapi_pagination import Page, Params

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.positionsDAO import PositionDAO
from src.schemas.positions_schemas import PositionCreateSchema, PositionReadSchema, PositionUpdateSchema
from src.utils.exceptions import (
    PositionAlreadyExistsException,
    PositionNotFoundException,
)


class PositionService:
    """Сервис для работы с должностями"""

    def __init__(self, db_helper, position_dao: PositionDAO, permissions_dao: PermissionsDAO):
        self.db_helper = db_helper
        self.position_dao = position_dao
        self.perm_dao = permissions_dao

    async def get_positions(
        self,
        params: Params,
        owner_id: int | None = None,
    ) -> Page[PositionReadSchema]:
        """Возвращает список всех должностей с возможностью отфильтровать по owner_id"""

        positions = await self.position_dao.get_positions(owner_id=owner_id, params=params)

        if positions.total == 0:
            raise PositionNotFoundException("Не найдено ни одной должности.")

        positions.items = [PositionReadSchema.model_validate(pos) for pos in positions.items]
        return positions

    async def get_position(
        self,
        position_id: int,
    ) -> PositionReadSchema:
        """Возвращает одну должность по id"""
        position = await self.position_dao.get_by_id(id=position_id)

        if not position:
            raise PositionNotFoundException("Должность с таким id не найдена.")

        return PositionReadSchema.model_validate(position)

    async def create_position(
        self,
        data: PositionCreateSchema,
    ) -> PositionReadSchema:
        """Создает новую должность"""

        payload = {
            "title": data.title,
            "owner_id": data.owner_id,
        }

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                position = await self.position_dao.get_position(
                    title=data.title,
                    owner_id=data.owner_id,
                    session=session,
                )

                if position:
                    raise PositionAlreadyExistsException("Должность с таким именем уже существует.")

                position = await self.position_dao.create(
                    payload=payload,
                    session=session,
                )
                if data.permissions:
                    await self.perm_dao.add_permissions_to_position(
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
        data: PositionUpdateSchema,
    ) -> PositionReadSchema:
        """Обновляет имя и права долджности"""

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                already_exists = await self.position_dao.get_position(
                    id=position_id,
                    session=session,
                )
                if not already_exists:
                    raise PositionNotFoundException("Должность с таким id не найдена.")

                if data.title:
                    updated = await self.position_dao.update(
                        position_id=position_id,
                        title=data.title,
                        session=session,
                    )

                if data.permissions_ids is not None:
                    await self.perm_dao.set_permissions_for_position(
                        position_id=position_id,
                        new_permission_ids=data.permissions_ids,
                        session=session,
                    )
                if updated:
                    result = updated
                else:
                    result = await self.position_dao.get_position(id=position_id, session=session)
                return PositionReadSchema.model_validate(result)

    async def delete_position(self, position_id: int) -> None:
        """Метод удалаяет должность по id"""

        await self.position_dao.delete(id=position_id)
