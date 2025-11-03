from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzsDAO import PVZsDAO
from src.schemas.employees_schemas import EmployeeResponseSchema
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate
from src.utils.exceptions import (
    EmployeeNotAllowedException,
    EmployeeNotFoundException,
    NoEmployeesInPVZException,
    PVZAlreadyExistsException,
    PVZDeleteFailedException,
    PVZNotFoundException,
)


class PVZService:
    async def add_pvz(
        self,
        data: PVZAdd,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(code=data.code)
        if pvz:
            raise PVZAlreadyExistsException("ПВЗ с таким кодом уже существует")

        payload = {
            "code": data.code,
            "type": data.type,
            "address": data.address,
            "group": data.group,
            "owner_id": data.owner_id,
            "curator_id": data.curator_id,
        }

        pvz_add = await repo.create(payload)
        return PVZRead(
            id=pvz_add.id,
            code=pvz_add.code,
            type=pvz_add.type,
            address=pvz_add.address,
            owner_id=pvz_add.owner_id,
            group=pvz_add.group,
            curator_id=pvz_add.curator_id,
            created_at=pvz_add.created_at,
        )

    async def update_pvz_by_id(
        self,
        pvz_id: int,
        data: PVZUpdate,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise PVZNotFoundException("ПВЗ с таким id не найдено")
        payload = {
            "address": data.address,
            "owner_id": data.owner_id,
            "curator_id": data.curator_id,
            "group": data.group,
        }
        pvz_update = await repo.update(id=pvz_id, **payload)

        return PVZRead(
            id=pvz_update.id,
            code=pvz_update.code,
            type=pvz_update.type,
            address=pvz_update.address,
            owner_id=pvz_update.owner_id,
            group=pvz_update.group,
            curator_id=pvz_update.curator_id,
            created_at=pvz_update.created_at,
        )

    async def get_pvz_by_id(
        self,
        pvz_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise PVZNotFoundException("ПВЗ с таким id не найдено")

        return PVZRead(
            id=pvz.id,
            code=pvz.code,
            type=pvz.type,
            address=pvz.address,
            owner_id=pvz.owner_id,
            group=pvz.group,
            curator_id=pvz.curator_id,
            created_at=pvz.created_at,
        )

    async def get_pvzs(
        self,
        code: str,
        type: str,
        address: str,
        group: str,
        repo: PVZsDAO,
    ) -> list[PVZRead]:
        filters = {}
        if code is not None:
            filters["code"] = code
        if type is not None:
            filters["type"] = type
        if address is not None:
            filters["address"] = address
        if group is not None:
            filters["group"] = group
        pvzs = await repo.get_pvzs(**filters)

        return [
            PVZRead(
                id=pvz.id,
                code=pvz.code,
                type=pvz.type,
                address=pvz.address,
                owner_id=pvz.owner_id,
                group=pvz.group,
                curator_id=pvz.curator_id,
                created_at=pvz.created_at,
            )
            for pvz in pvzs
        ]

    async def delete_pvz_by_id(
        self,
        pvz_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise PVZNotFoundException("ПВЗ с таким id не найдено")
        pvz_info = {
            "id": pvz.id,
            "code": pvz.code,
            "type": pvz.type,
            "address": pvz.address,
            "owner_id": pvz.owner_id,
            "group": pvz.group,
            "curator_id": pvz.curator_id,
            "created_at": pvz.created_at,
        }
        success = await repo.delete(id=pvz_id)
        if not success:
            raise PVZDeleteFailedException("Ошибка при удалении ПВЗ")

        return pvz_info

    async def get_employees_by_pvz_checked(
        self,
        user_id: int,
        pvz_id: int,
        repo: EmployeesDAO,
        pvz_repo: PVZsDAO,
    ) -> list[EmployeeResponseSchema]:
        """
        Возвращает список сотрудников указанного ПВЗ, если запрашивающий сотрудник
        действительно привязан к этому ПВЗ.
        """
        employee = await repo.get_employee(user_id=user_id)
        if not employee:
            raise EmployeeNotFoundException("Сотрудник не найден")

        # Проверка, что сотрудник действительно привязан к указанному ПВЗ
        if not any(pvz.id == pvz_id for pvz in employee.pvzs):
            raise EmployeeNotAllowedException("Нет доступа к этому ПВЗ")

        # Получаем всех сотрудников данного ПВЗ
        employees = await pvz_repo.get_employees_by_pvz_id(pvz_id=pvz_id)
        if not employees:
            raise NoEmployeesInPVZException("В ПВЗ нет сотрудников")

        return [EmployeeResponseSchema.model_validate(e) for e in employees]
