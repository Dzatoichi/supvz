from fastapi_pagination import Page, Params, paginate

from src.dao.permissionsDAO import PermissionsDAO
from src.dao.positionsDAO import PositionDAO
from src.models import Positions
from src.schemas.perm_positions_schemas import PositionCreateSchema, PositionReadSchema
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
    ) -> Positions:
        position = await repo.get_by_id(id=position_id)

        if not position:
            raise PositionNotFoundException("Должность с таким id не найдена.")

        return position

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
