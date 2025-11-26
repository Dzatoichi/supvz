from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from src.dao.positionsDAO import PositionDAO
from src.schemas.perm_positions_schemas import PositionReadSchema
from src.services.position_service import PositionService

positions_router = APIRouter(prefix="/positions", tags=["Position"])


@positions_router.get("/")
async def get_positions(
    position_service: PositionService = Depends(get_position_service),
    repo: PositionDAO = Depends(get_position_dao),
    page_params: Params = Depends(),
) -> Page[PositionReadSchema]:
    """Ручка для получения должностей"""

    positions = await position_service.get_positions(repo=repo, params=page_params)
    return positions


@positions_router.get("/{position_id}")
async def get_position(
    position_id: int,
    position_service: PositionService = Depends(get_position_service),
    repo: PositionDAO = Depends(get_position_dao),
    page_params: Params = Depends(),
) -> PositionReadSchema:
    position = await position_service.get_position(
        position_id=position_id,
        repo=repo,
        params=page_params,
    )
    return position
