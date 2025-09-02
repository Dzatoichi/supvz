from auth_service.src.dao.baseDAO import BaseDAO
from auth_service.src.models.pvzs.PVZs import PVZs


class PVZsDAO(BaseDAO[PVZs]):
    def __init__(self):
        super().__init__(model=PVZs)
