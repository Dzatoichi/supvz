from datetime import datetime

from fastapi import HTTPException
from fastapi_pagination import Page, Params

from src.dao import ScheduledShiftsDAO
from src.schemas.scheduled_shifts_schemas import (
    ScheduledShiftCreateSchema,
    ScheduledShiftReadSchema,
    ScheduledShiftUpdateSchema,
)
from src.utils.logger_settings import logger


class ScheduledShiftsService:
    """
    Сервис для работы с Scheduled Shifts
    """

    async def create_scheduled_shift(
        self, scheduled_shift_data: ScheduledShiftCreateSchema, repo: ScheduledShiftsDAO
    ) -> ScheduledShiftReadSchema:
        """
        Создание запланированной схемы
        """

        payload = {
            "pvz_id": scheduled_shift_data.pvz_id,
            "user_id": scheduled_shift_data.user_id,
            "starts_at": scheduled_shift_data.starts_at,
            "ends_at": scheduled_shift_data.ends_at,
        }
        scheduled_shift = await repo.create(payload=payload)
        return ScheduledShiftReadSchema.model_validate(scheduled_shift)

    async def get_scheduled_shifts(
        self,
        user_id: int | None,
        pvz_id: int | None,
        starts_at: datetime | None,
        ends_at: datetime | None,
        completed: bool | None,
        status: str | None,
        paid: bool | None,
        repo: ScheduledShiftsDAO,
        params: Params,
    ) -> Page[ScheduledShiftReadSchema]:
        """
        Получение всех запланированных схем с фильтрацией и пагинацией
        """

        scheduled_shifts = await repo.get_scheduled_shifts_filtered(
            user_id=user_id,
            pvz_id=pvz_id,
            starts_at=starts_at,
            ends_at=ends_at,
            completed=completed,
            status=status,
            paid=paid,
            params=params,
        )
        scheduled_shifts.items = [
            ScheduledShiftReadSchema.model_validate(scheduled_shift) for scheduled_shift in scheduled_shifts.items
        ]
        return scheduled_shifts

    async def get_scheduled_shift_by_id(
        self, scheduled_shift_id: int, repo: ScheduledShiftsDAO
    ) -> ScheduledShiftReadSchema:
        """
        Получение запланированной смены по ID
        """

        scheduled_shift = await repo.get_by_id(scheduled_shift_id)
        if not scheduled_shift:
            raise HTTPException(status_code=404, detail="Смена не найдена")

        return ScheduledShiftReadSchema.model_validate(scheduled_shift)

    async def update_scheduled_shift(
        self, scheduled_shift_id: int, updated_data: ScheduledShiftUpdateSchema, repo: ScheduledShiftsDAO
    ) -> ScheduledShiftReadSchema:
        """
        Обновляет данные запланированной схемы
        """

        update_scheduled_shift = await repo.get_by_id(scheduled_shift_id)
        if not update_scheduled_shift:
            raise HTTPException(status_code=404, detail="Смена не найдена")

        update_fields = {}
        if updated_data.pvz_id is not None:
            update_fields["pvz_id"] = updated_data.pvz_id
        if updated_data.user_id is not None:
            update_fields["user_id"] = updated_data.user_id
        if updated_data.starts_at is not None:
            update_fields["starts_at"] = updated_data.starts_at
        if updated_data.ends_at is not None:
            update_fields["ends_at"] = updated_data.ends_at
        if updated_data.completed is not None:
            update_fields["completed"] = updated_data.completed
        if updated_data.status is not None:
            update_fields["status"] = updated_data.status
        if updated_data.paid is not None:
            update_fields["paid"] = updated_data.paid

        updated_scheduled_shift = await repo.update(id=scheduled_shift_id, **update_fields)

        if updated_scheduled_shift:
            logger.info(
                "Запланированная смена id=%s успешно обновлена!",
                updated_scheduled_shift.id,
            )
            return ScheduledShiftReadSchema.model_validate(updated_scheduled_shift)
        else:
            raise HTTPException(status_code=400, detail="Невалидные параметры смены")

    async def delete_scheduled_shift(self, scheduled_shift_id: int, repo: ScheduledShiftsDAO) -> None:
        """
        Удаление запланированной смены
        """

        scheduled_shift = await repo.get_by_id(scheduled_shift_id)
        if not scheduled_shift:
            raise HTTPException(status_code=404, detail="Scheduled shift not found")

        logger.info(
            "Запланированная смена id={scheduled_shift_id} успешно удалена!",
            scheduled_shift_id=scheduled_shift.id,
        )

        await repo.delete(scheduled_shift.id)
