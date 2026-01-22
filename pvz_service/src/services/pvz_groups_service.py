from sqlalchemy.exc import IntegrityError

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.policies.pvz_group_policy import PVZGroupAccessPolicy
from src.schemas.pvz_group_schemas import (
    PVZGroupCreateSchema,
    PVZGroupResponseSchema,
    PVZGroupUpdateSchema,
)
from src.utils.exceptions import (
    EmployeeNotFoundException,
    PVZGroupAlreadyExistsException,
    PVZGroupNotFoundException,
)


class PVZGroupsService:
    """
    Сервис для работы с группами ПВЗ.
    """

    def __init__(
        self,
        db_helper,
        group_policy: PVZGroupAccessPolicy,
        group_repo: PVZGroupsDAO,
        pvz_repo: PVZsDAO,
        employee_repo: EmployeesDAO,
    ):
        self.db_helper = db_helper
        self.group_policy = group_policy
        self.group_repo = group_repo
        self.pvz_repo = pvz_repo
        self.employee_repo = employee_repo

    async def create_group(
        self,
        data: PVZGroupCreateSchema,
        current_user_id: int,
    ):
        """Создаёт новую группу ПВЗ"""

        existing_group = await self.group_repo.get_group(name=data.name, owner_id=current_user_id)
        if existing_group:
            raise PVZGroupAlreadyExistsException("Группа с таким именем уже существует")

        owner_exists = await self.employee_repo.get_employee(user_id=current_user_id)
        if not owner_exists:
            raise EmployeeNotFoundException(f"Owner с user_id={current_user_id} не существует")

        payload = data.model_dump()
        payload["owner_id"] = current_user_id

        group = await self.group_repo.create(payload)

        return PVZGroupResponseSchema.model_validate(group)

    async def update_group(
        self,
        group_id: int,
        data: PVZGroupUpdateSchema,
        current_user_id: int,
    ):
        """Обновляет данные группы ПВЗ и кураторство для ПВЗ при необходимости."""

        await self.group_policy.check_group_access(group_id, current_user_id)

        existing_group = await self.group_repo.get_by_id(id=group_id)
        if not existing_group:
            raise PVZGroupNotFoundException("Группы с таким id не существет")

        try:
            group = await self.group_repo.update(group_id, **data.model_dump(exclude_unset=True))
        except IntegrityError:
            raise PVZGroupAlreadyExistsException("Группа с таким именем уже существует") from None

        if data.responsible_id:
            await self.pvz_repo.update_pvzs_responsible_by_group(group_id, data.responsible_id)

        return PVZGroupResponseSchema.model_validate(group)

    async def get_groups(
        self,
        responsible_id: int,
        current_user_id: int,
    ) -> list[PVZGroupResponseSchema] | PVZGroupResponseSchema:
        """Возвращает группы по owner_id или responsible_id."""

        filters = {"owner_id": current_user_id}

        if responsible_id is not None:
            filters["responsible_id"] = responsible_id

        groups = await self.group_repo.get_groups(**filters)

        if not groups:
            raise PVZGroupNotFoundException("Группы не найдены")

        return [PVZGroupResponseSchema.model_validate(g) for g in groups]

    async def get_group_with_pvzs(
        self,
        group_id: int,
        current_user_id: int,
    ):
        """Возвращает одну группу ПВЗ по ID с информацией о ПВЗ."""

        await self.group_policy.check_group_access(group_id, current_user_id)

        group = await self.group_repo.get_by_id(group_id)

        if not group:
            raise PVZGroupNotFoundException("Группа не найдена")

        return PVZGroupResponseSchema.model_validate(group)

    async def delete_group(
        self,
        group_id: int,
        current_user_id: int,
    ):
        """Удаляет группу ПВЗ."""

        await self.group_policy.check_group_access(group_id, current_user_id)

        existing_group = await self.group_repo.get_by_id(id=group_id)
        if not existing_group:
            raise PVZGroupNotFoundException("Группы с таким id не существет")

        await self.group_repo.delete(id=group_id)

    async def assign_responsible(
        self,
        group_id: int,
        responsible_id: int,
        current_user_id: int,
    ):
        """Привязывает куратора к группе, а также ко всем пвз состоящим в этой группе"""

        await self.group_policy.check_group_access(group_id, current_user_id)

        existing_group = await self.group_repo.get_by_id(id=group_id)
        if not existing_group:
            raise PVZGroupNotFoundException("Группы с таким id не существет")

        async with self.db_helper.async_session_maker() as session:
            async with session.begin():
                await self.group_repo.set_responsible(group_id, responsible_id, session)
                await self.pvz_repo.set_responsible_for_group(group_id, responsible_id, session)

        return {"detail": "Куратор успешно назначен и применён ко всем ПВЗ группы"}
