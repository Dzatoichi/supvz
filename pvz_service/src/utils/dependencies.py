from src.dao.pvzsDAO import PVZsDAO
from src.services.pvz_service import PVZService


def get_pvzs_service() -> PVZService:
    return PVZService()

def get_pvzs_dao() -> PVZsDAO:
    return PVZsDAO()
