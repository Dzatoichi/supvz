from fastapi import HTTPException, status

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.models.pvzs.PVZs import PVZs
from src.schemas.employees_schemas import EmployeeResponseSchema
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate


class PVZService:
    async def add_pvz(
        self,
        data: PVZAdd,
        repo: PVZsDAO,
        group_repo: PVZGroupsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(code=data.code)
        if pvz:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"PVZ с кодом {data.code} уже существует",
            )

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
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pvz not found")

        pvz_update = await repo.update(id=pvz_id, **data.model_dump(exclude_unset=True))

        return PVZRead.model_validate(pvz_update)

    async def get_pvz_by_id(
        self,
        pvz_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pvz not found")

        return PVZRead.model_validate(pvz)

    async def get_pvzs(
        self,
        code: str,
        type: str,
        address: str,
        repo: PVZsDAO,
        group_id: int | None = None,
    ) -> list[PVZRead]:
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

        return [PVZRead.model_validate(pvz) for pvz in pvzs]

    async def delete_pvz_by_id(
        self,
        pvz_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pvz not found")
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
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete PVZ")

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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сотрудник с user_id={user_id} не найден.",
            )

        # Проверка, что сотрудник действительно привязан к указанному ПВЗ
        if not any(pvz.id == pvz_id for pvz in employee.pvzs):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете просматривать сотрудников этого ПВЗ.",
            )

        # Получаем всех сотрудников данного ПВЗ
        employees = await pvz_repo.get_employees_by_pvz_id(pvz_id=pvz_id)
        if not employees:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"В ПВЗ с id={pvz_id} не найдено сотрудников.",
            )

        return [EmployeeResponseSchema.model_validate(e) for e in employees]

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
