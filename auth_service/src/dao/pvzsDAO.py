from src.dao.baseDAO import BaseDAO
from src.models.pvzs.PVZs import PVZs


class PVZsDAO(BaseDAO[PVZs]):
    def __init__(self):
        super().__init__(model=PVZs)
