from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.dao.pvzsDAO import PVZsDAO
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate
from src.services.pvz_service import PVZService
from src.utils.dependencies import get_pvz_repo, get_pvz_service

pvz_router = APIRouter(prefix="/pvzs", tags=["pvzs"])


@pvz_router.post("/", response_model=PVZRead)
async def add_pvz(
    pvz_in: PVZAdd,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Создаёт новый пункт выдачи заказов (ПВЗ)."""

    pvz = await pvz_service.add_pvz(data=pvz_in, repo=repo)

    return pvz


@pvz_router.patch("/{pvz_id}", response_model=PVZRead)
async def update_pvz_by_id(
    pvz_id: int,
    pvz_in: PVZUpdate,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Обновляет данные существующего ПВЗ по его идентификатору."""

    pvz = await pvz_service.update_pvz_by_id(pvz_id=pvz_id, data=pvz_in, repo=repo)
    return pvz


@pvz_router.get("/{pvz_id}", response_model=PVZRead)
async def get_pvz_by_id(
    pvz_id: int,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Возвращает информацию о конкретном ПВЗ по его идентификатору."""

    pvz = await pvz_service.get_pvz_by_id(pvz_id=pvz_id, repo=repo)
    return pvz


@pvz_router.get("/", response_model=list[PVZRead])
async def get_pvzs(
    code: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    group: Optional[str] = Query(None),
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Возвращает список всех ПВЗ с возможностью фильтрации по коду, типу, адресу или группе."""

    pvzs = await pvz_service.get_pvzs(
        code=code,
        type=type,
        address=address,
        group=group,
        repo=repo,
    )
    return pvzs


@pvz_router.delete("/{pvz_id}", response_model=PVZRead)
async def delete_pvz_by_id(
    pvz_id: int,
    repo: PVZsDAO = Depends(get_pvz_repo),
    pvz_service: PVZService = Depends(get_pvz_service),
):
    """Удаляет ПВЗ по его идентификатору."""

    result = await pvz_service.delete_pvz_by_id(pvz_id=pvz_id, repo=repo)
    return result
