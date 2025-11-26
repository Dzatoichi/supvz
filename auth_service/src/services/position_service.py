from fastapi import HTTPException, status
from fastapi_pagination import Page, Params, paginate

from src.dao.positionsDAO import PositionDAO
from src.schemas.perm_positions_schemas import PositionCreateSchema, PositionReadSchema


class PositionService:
    """Сервис для работы с должностями"""

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return PositionReadSchema.model_validate(position)

    async def create_position(
        self,
        data: PositionCreateSchema,
    ) -> PositionReadSchema:
        """Создает новую должность"""
        pass
