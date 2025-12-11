from fastapi import HTTPException, status
from fastapi_pagination import Page, Params, paginate

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.models.pvzs.PVZs import PVZs
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
        group_repo: PVZGroupsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(code=data.code)
        if pvz:
            raise PVZAlreadyExistsException("ПВЗ с таким кодом уже существует")

        # Если указан group_id, проверяем владельца
        if data.group_id == 0:
            data.group_id = None
        elif data.group_id:
            group = await group_repo.get_group(id=data.group_id)
            if not group:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail=f"Группа {data.group_id} не найдена",
                )

            # Проверяем, что owner_id ПВЗ совпадает с owner_id группы
            if data.owner_id != group.owner_id:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Невозможно добавить ПВЗ: owner_id={data.owner_id} "
                        f"не совпадает с owner_id группы={group.owner_id}"
                    ),
                )

        pvz_add = await repo.create(data.model_dump())
        return PVZRead.model_validate(pvz_add, from_attributes=True)

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
            "group_id": data.group_id,
        }
        pvz_update = await repo.update(id=pvz_id, **payload)

        return PVZRead(
            id=pvz_update.id,
            code=pvz_update.code,
            type=pvz_update.type,
            address=pvz_update.address,
            owner_id=pvz_update.owner_id,
            group_id=pvz_update.group_id,
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

        return PVZRead.model_validate(pvz)

    async def get_pvzs(
        self,
        code: str,
        type: str,
        address: str,
        repo: PVZsDAO,
        params: Params,
        group_id: int | None = None,
    ) -> Page[PVZRead]:
        filters = {}
        if code is not None:
            filters["code"] = code
        if type is not None:
            filters["type"] = type
        if address is not None:
            filters["address"] = address
        if group_id is not None:
            filters["group_id"] = group_id

        pvzs = await repo.get_pvzs(**filters)

        pvzs_page = paginate(pvzs, params=params)

        # конвертация ORM -> Pydantic
        pvzs_page.items = [PVZRead.model_validate(pvz) for pvz in pvzs_page.items]

        return pvzs_page

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
        params: Params,
    ) -> Page[EmployeeResponseSchema]:
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
        employees_page = await pvz_repo.get_employees_by_pvz_id(pvz_id=pvz_id, params=params)
        if not employees_page.items:
            raise NoEmployeesInPVZException("В ПВЗ нет сотрудников")

        # конвертируем ORM -> Pydantic
        employees_page.items = [EmployeeResponseSchema.model_validate(e) for e in employees_page.items]

        return employees_page

    async def assign_pvz_to_group(
        self,
        group_id: int,
        pvz_ids: list[int],
        repo: PVZGroupsDAO,
        pvz_repo: PVZsDAO,
    ):
        group = await repo.get_group(id=group_id)
        if not group:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Группа не найдена")

        # Получаем все ПВЗ, которые хотим привязать
        pvzs = await pvz_repo.get_pvzs(PVZs.id.in_(pvz_ids))

        if len(pvzs) != len(pvz_ids):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Некоторые ПВЗ не существуют")

        # Проверяем, что у всех ПВЗ owner_id совпадает с owner_id группы
        for pvz in pvzs:
            if pvz.owner_id != group.owner_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ПВЗ {pvz.id} принадлежит другому владельцу",
                )

        await pvz_repo.assign_pvz_to_group(group_id=group_id, pvz_ids=pvz_ids)

        return {"detail": "ПВЗ успешно привязаны к группе"}

    async def unassign_all_pvz_from_group(
        self,
        group_id,
        pvz_repo: PVZsDAO,
    ):
        """Отвязывает все ПВЗ от группы."""

        await pvz_repo.unassign_pvzs_from_group(group_id)
