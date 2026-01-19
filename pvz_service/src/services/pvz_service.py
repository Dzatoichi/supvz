from fastapi_pagination import Page, Params

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.models.pvzs.PVZs import PVZs
from src.policies.pvz_policy import PVZAccessPolicy
from src.schemas.employees_schemas import EmployeeResponseSchema
from src.schemas.pvz_schemas import PVZAdd, PVZRead, PVZUpdate
from src.utils.exceptions import (
    AccessDeniedException,
    EmployeeNotAllowedException,
    EmployeeNotFoundException,
    NoEmployeesInPVZException,
    PVZAlreadyExistsException,
    PVZDeleteFailedException,
    PVZGroupNotFoundException,
    PVZNotFoundException,
)


class PVZService:
    """
    Сервис для работы с ПВЗ.
    """

    def __init__(
        self,
        pvz_policy: PVZAccessPolicy,
    ):
        self.pvz_policy = pvz_policy

    async def add_pvz(
        self,
        data: PVZAdd,
        current_user_id: int,
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
                raise PVZGroupNotFoundException(f"Группа {data.group_id} не найдена")

            if group.owner_id != current_user_id:
                raise AccessDeniedException("Нельзя привязать ПВЗ к чужой группе.")

        payload = data.model_dump()
        payload["owner_id"] = current_user_id
        pvz_add = await repo.create(payload)

        return PVZRead.model_validate(pvz_add, from_attributes=True)

    async def update_pvz_by_id(
        self,
        pvz_id: int,
        current_user_id: int,
        data: PVZUpdate,
        repo: PVZsDAO,
        group_repo: PVZGroupsDAO,
    ) -> PVZRead:
        await self.pvz_policy.check_pvz_access(pvz_id, current_user_id)

        # Если меняем группу, проверяем права на новую группу
        if data.group_id:
            group = await group_repo.get_group(id=data.group_id)
            if not group:
                raise PVZGroupNotFoundException("Группа не найдена")
            if group.owner_id != current_user_id:
                raise AccessDeniedException("Нет прав на указанную группу")

        payload = {
            "address": data.address,
            "responsible_id": data.responsible_id,
            "group_id": data.group_id,
            "type": data.type,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        pvz_update = await repo.update(id=pvz_id, **payload)
        return PVZRead.model_validate(pvz_update)

    async def get_pvz_by_id(
        self,
        pvz_id: int,
        current_user_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        await self.pvz_policy.check_pvz_access(pvz_id, current_user_id)

        pvz = await repo.get_pvz(id=pvz_id)
        if not pvz:
            raise PVZNotFoundException("ПВЗ не найден")

        return PVZRead.model_validate(pvz)

    async def get_pvzs(
        self,
        current_user_id: int,
        code: str,
        type: str,
        address: str,
        repo: PVZsDAO,
        params: Params,
        group_id: int | None = None,
    ) -> Page[PVZRead]:
        filters = {"owner_id": current_user_id}

        if code is not None:
            filters["code"] = code
        if type is not None:
            filters["type"] = type
        if address is not None:
            filters["address"] = address
        if group_id is not None:
            filters["group_id"] = group_id

        pvzs = await repo.get_pvzs(params=params, **filters)

        pvzs.items = [PVZRead.model_validate(pvz) for pvz in pvzs.items]

        return pvzs

    async def delete_pvz_by_id(
        self,
        pvz_id: int,
        current_user_id: int,
        repo: PVZsDAO,
    ) -> PVZRead:
        await self.pvz_policy.check_pvz_access(pvz_id, current_user_id)

        pvz = await repo.get_pvz(id=pvz_id)

        result_data = {
            "id": pvz.id,
            "code": pvz.code,
            "type": pvz.type,
            "address": pvz.address,
            "owner_id": pvz.owner_id,
            "group_id": pvz.group_id,
            "responsible_id": pvz.responsible_id,
            "created_at": pvz.created_at,
        }

        success = await repo.delete(id=pvz_id)
        if not success:
            raise PVZDeleteFailedException("Ошибка при удалении ПВЗ")

        return PVZRead(**result_data)

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
        current_user_id: int,
        repo: PVZGroupsDAO,
        pvz_repo: PVZsDAO,
    ):
        group = await repo.get_group(id=group_id)
        if not group:
            raise PVZGroupNotFoundException("Группа не найдена")

        # Получаем все ПВЗ, которые хотим привязать
        pvzs = await pvz_repo.get_pvzs(
            Params(size=len(pvz_ids)),
            PVZs.id.in_(pvz_ids),
            owner_id=current_user_id,
        )

        if len(pvzs.items) != len(pvz_ids):
            raise PVZAlreadyExistsException("Некоторые ПВЗ не существуют")

        await pvz_repo.assign_pvz_to_group(group_id=group_id, pvz_ids=pvz_ids)

        return {"detail": "ПВЗ успешно привязаны к группе"}

    async def unassign_all_pvz_from_group(
        self,
        group_id,
        pvz_repo: PVZsDAO,
    ):
        """Отвязывает все ПВЗ от группы."""

        await pvz_repo.unassign_pvzs_from_group(group_id)
