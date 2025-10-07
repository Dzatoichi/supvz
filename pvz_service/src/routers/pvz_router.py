from fastapi import APIRouter, Depends

from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_schemas import PVZBase, PVZGroup, PVZAdd, PVZUpdate, PVZRead, PVZGet
from src.services.pvz_service import PVZService
from src.utils.dependencies import get_pvzs_dao, get_pvzs_service

pvz_router = APIRouter(prefix="/pvz")

@pvz_router.post("/add-pvz", response_model=PVZRead)
async def add_pvz(
    pvz_in: PVZAdd,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvz = await pvz_service.add_pvz(data=pvz_in, repo=repo)

    return pvz

@pvz_router.put("/update-pvz/{pvz_id}", response_model=PVZRead)
async def update_pvz_by_id(
    pvz_id: int,
    pvz_in: PVZUpdate,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvz = await pvz_service.update_pvz_by_id(pvz_id=pvz_id, data=pvz_in, repo=repo)
    return pvz

@pvz_router.get("/get-pvz/{pvz_id}", response_model=PVZRead)
async def get_pvz_by_id(
    pvz_id: int,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvz = await pvz_service.get_pvz_by_id(pvz_id=pvz_id, repo=repo)
    return pvz

@pvz_router.get("/get-pvzs", response_model=list[PVZRead])
async def get_pvzs(
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvzs = await pvz_service.get_pvzs(repo=repo)

    return pvzs

@pvz_router.delete("/delete/{pvz_id}", response_model=PVZRead)
async def delete_pvz_by_id(
    pvz_id: int,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    result = await pvz_service.delete_pvz_by_id(pvz_id=pvz_id, repo=repo)
    return result
