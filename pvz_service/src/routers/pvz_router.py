from fastapi import APIRouter, Depends

from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_schemas import PVZBase, PVZGroup
from src.services.pvz_service import PVZService
from src.utils.dependencies import get_pvzs_dao, get_pvzs_service

pvz_router = APIRouter(prefix="/pvz")

@pvz_router.post("/add-group", response_model=PVZBase)
async def add_group(
    pvz_in: PVZGroup,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvz = await pvz_service.add_group(pvz_in, repo)

    return pvz
