from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.services.pvz_groups_service import PVZGroupsService
from src.services.pvz_service import PVZService


def get_pvzs_service() -> PVZService:
    return PVZService()


def get_pvzs_dao() -> PVZsDAO:
    return PVZsDAO()


def get_pvz_groups_service() -> PVZGroupsService:
    return PVZGroupsService()


def get_pvz_groups_repo() -> PVZGroupsDAO:
    return PVZGroupsDAO()
