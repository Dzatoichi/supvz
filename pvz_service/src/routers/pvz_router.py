from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate
from src.services.pvz_service import PVZService
from src.utils.dependencies import get_pvz_groups_repo, get_pvzs_dao, get_pvzs_service

pvz_router = APIRouter(prefix="/pvzs", tags=["pvzs"])


@pvz_router.post("/", response_model=PVZRead)
async def add_pvz(
    pvz_in: PVZAdd,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
    group_repo: PVZGroupsDAO = Depends(get_pvz_groups_repo),
):
    pvz = await pvz_service.add_pvz(data=pvz_in, repo=repo, group_repo=group_repo)

    return pvz


@pvz_router.patch("/{pvz_id}", response_model=PVZRead)
async def update_pvz_by_id(
    pvz_id: int,
    pvz_in: PVZUpdate,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvz = await pvz_service.update_pvz_by_id(pvz_id=pvz_id, data=pvz_in, repo=repo)
    return pvz


@pvz_router.get("/{pvz_id}", response_model=PVZRead)
async def get_pvz_by_id(
    pvz_id: int,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvz = await pvz_service.get_pvz_by_id(pvz_id=pvz_id, repo=repo)
    return pvz


@pvz_router.get("/", response_model=list[PVZRead])
async def get_pvzs(
    code: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    group_id: Optional[int] = Query(None),
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    pvzs = await pvz_service.get_pvzs(
        code=code,
        type=type,
        address=address,
        group_id=group_id,
        repo=repo,
    )
    return pvzs


@pvz_router.delete("/{pvz_id}", response_model=PVZRead)
async def delete_pvz_by_id(
    pvz_id: int,
    repo: PVZsDAO = Depends(get_pvzs_dao),
    pvz_service: PVZService = Depends(get_pvzs_service),
):
    result = await pvz_service.delete_pvz_by_id(pvz_id=pvz_id, repo=repo)
    return result
