from datetime import datetime

from fastapi import HTTPException, status

from src.schemas.pvz_schemas import PVZRead


class FakePVZService:
    """
    Это фейковый сервис, который имитирует поведение настоящего PVZService
    для использования в API-тестах. Он не ходит в базу данных.
    """
    
    _fake_db = [
        PVZRead(id=1, code="PVZ-MSK-01", type="ozon", address="Москва", owner_id=10, group="A", curator_id=1, created_at=datetime.utcnow()),
        PVZRead(id=2, code="PVZ-SPB-01", type="wb", address="Санкт-Петербург", owner_id=11, group="A", curator_id=2, created_at=datetime.utcnow()),
        PVZRead(id=3, code="PVZ-MSK-02", type="ozon", address="Москва, ул. Тверская", owner_id=12, group="B", curator_id=3, created_at=datetime.utcnow()),
    ]

    async def add_pvz(self, data, repo):
        
        if data.code == "EXISTING-CODE":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pvz already exists",
            )
        return PVZRead(id=1, created_at=datetime.now(), **data.model_dump())

    async def get_pvz_by_id(self, pvz_id, repo):
        if pvz_id == 999:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pvz not found",
            )
            
        return PVZRead(
            id=pvz_id,
            code="FETCHED-PVZ",
            type="ozon",
            address="Fetched Address",
            owner_id=1,
            group="A",
            curator_id=1,
            created_at=datetime.now()
        )

    async def update_pvz_by_id(self, pvz_id, data, repo):
        if pvz_id == 999:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pvz not found",
            )
        return PVZRead(
            id=pvz_id,
            code="FETCHED-PVZ-UPDATED",
            type="ozon",
            address="Fetched Address_1",
            owner_id=data.owner_id,
            group=data.group,
            curator_id=data.curator_id,
            created_at=datetime.now()
        )

    async def get_pvzs(self, code, type, address, group, repo):
        results = self._fake_db

        if code is not None:
            results = [pvz for pvz in results if pvz.code == code]
        
        if type is not None:
            results = [pvz for pvz in results if pvz.type == type]
            
        if address is not None:
            results = [pvz for pvz in results if address in pvz.address]

        if group is not None:
            results = [pvz for pvz in results if pvz.group == group]

        return results

    async def delete_pvz_by_id(
        self,
        pvz_id,
        repo,
    ):
        if pvz_id == 999:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pvz not found",
            )
        return PVZRead(
            id=pvz_id,
            code="DELETED-PVZ",
            type="ozon",
            address="Fetched Address_1",
            owner_id=10,
            group="A",
            curator_id=1,
            created_at=datetime.now(),
        )
