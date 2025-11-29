from fastapi_pagination import Page, Params, paginate

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.positionsDAO import PositionDAO
from src.models import Positions
from src.schemas.perm_positions_schemas import PositionCreateSchema, PositionReadSchema, PositionUpdateSchema
from src.utils.exceptions import (
    PositionAlreadyExistsException,
    PositionNotFoundException,
)


class PositionService:
    """Сервис для работы с должностями"""

    def __init__(self, db_helper):
        self.db_helper = db_helper

    async def get_positions(
        self,
        repo: PositionDAO,
        params: Params,
        owner_id: int | None = None,
    ) -> Page[PositionReadSchema]:
        """Возвращает список всех должностей с возможностью отфильтровать по owner_id"""

        if owner_id is None:
            positions = await repo.get_all()
        else:
            positions = await repo.get_positions(owner_id=owner_id)

        if not positions:
            raise PositionNotFoundException("Не найдено ни одной должности.")

        positions_page = paginate(positions, params)

        positions_page.items = [PositionReadSchema.model_validate(position) for position in positions_page.items]

        return positions_page

    async def get_position(
        self,
        position_id: int,
        repo: PositionDAO,
    ) -> PositionReadSchema:
        position = await repo.get_by_id(id=position_id)

        if not position:
            raise PositionNotFoundException("Должность с таким id не найдена.")

        return PositionReadSchema.model_validate(position)

    async def create_position(
        self,
        data: PositionCreateSchema,
        position_repo: PositionDAO,
        permission_repo: PermissionsDAO,
    ) -> Positions:
        """Создает новую должность"""
        position = await position_repo.get_position(title=data.title, owner_id=data.owner_id)
        if position:
            raise PositionAlreadyExistsException("Должность с таким именем уже существует.")

        payload = {
            "title": data.title,
            "owner_id": data.owner_id,
        }

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                position = await position_repo.create(
                    payload,
                    session=session,
                )
                if data.permissions:
                    await permission_repo.add_permissions_to_position(
                        position_id=position.id,
                        permission_ids=data.permissions,
                        session=session,
                    )

                else:
                    position.permissions = None

                return position

    async def update_position(
        self,
        position_id: int,
        data: PositionUpdateSchema,
        position_repo: PositionDAO,
        permission_repo: PermissionsDAO,
    ) -> PositionReadSchema:
        """Обновляет имя и права долджности"""

        already_exists = await position_repo.get_by_id(id=position_id)

        if not already_exists:
            raise PositionNotFoundException("Должность с таким id не найдена.")

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                if data.title:
                    await position_repo.update(
                        position_id=position_id,
                        title=data.title,
                        session=session,
                    )

                if data.permissions_ids is not None:
                    await permission_repo.set_permissions_for_position(
                        position_id=position_id,
                        new_permission_ids=data.permissions_ids,
                        session=session,
                    )

                result = await position_repo.get_position(id=position_id)
                return PositionReadSchema.model_validate(result)

    async def delete_position(self, position_id: int, repo: PositionDAO):
        """Метод удалаяет должность по id"""

        return await repo.delete(id=position_id)
