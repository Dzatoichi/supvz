from datetime import datetime

from fastapi import HTTPException, status
from fastapi_pagination import Page, Params

from src.dao import ScheduledShiftsDAO
from src.schemas.scheduled_shifts_schemas import (
    ScheduledShiftCreateSchema,
    ScheduledShiftReadSchema,
    ScheduledShiftUpdateSchema,
)
from src.utils.exceptions import ScheduledShiftNotFoundException, ScheduledShiftValidationException
from src.utils.logger_settings import logger


class ScheduledShiftsService:
    """
    Сервис для работы с Scheduled Shifts
    """

    async def create_scheduled_shift(
        self,
        scheduled_shift_data: ScheduledShiftCreateSchema,
        repo: ScheduledShiftsDAO,
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
        self,
        scheduled_shift_id: int,
        repo: ScheduledShiftsDAO,
    ) -> ScheduledShiftReadSchema:
        """
        Получение запланированной смены по ID
        """

        scheduled_shift = await repo.get_by_id(scheduled_shift_id)
        if not scheduled_shift:
            raise ScheduledShiftNotFoundException("Смена не найдена")

        return ScheduledShiftReadSchema.model_validate(scheduled_shift)

    async def update_scheduled_shift(
        self,
        scheduled_shift_id: int,
        updated_data: ScheduledShiftUpdateSchema,
        repo: ScheduledShiftsDAO,
    ) -> ScheduledShiftReadSchema:
        """
        Обновляет данные запланированной схемы
        """

        update_scheduled_shift = await repo.get_by_id(scheduled_shift_id)
        if not update_scheduled_shift:
            raise ScheduledShiftNotFoundException("Смена не найдена")
        update_fields = {}
        updated_data_dict = dict(updated_data)
        for updated_field_name, updated_field_value in updated_data_dict.items():
            if updated_field_value is not None:
                update_fields[updated_field_name] = updated_field_value

        updated_scheduled_shift = await repo.update(id=scheduled_shift_id, **update_fields)

        if updated_scheduled_shift:
            logger.info(
                "Запланированная смена id=%s успешно обновлена!",
                updated_scheduled_shift.id,
            )
            return ScheduledShiftReadSchema.model_validate(updated_scheduled_shift)
        else:
            raise ScheduledShiftValidationException("Невалидные параметры схемы")

    async def delete_scheduled_shift(
        self,
        scheduled_shift_id: int,
        repo: ScheduledShiftsDAO,
    ) -> None:
        """
        Удаление запланированной смены
        """

        scheduled_shift = await repo.get_by_id(scheduled_shift_id)
        if not scheduled_shift:
            raise ScheduledShiftNotFoundException("Смена не найдена")

        success = await repo.delete(scheduled_shift.id)
        if not success:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.info(
            "Запланированная смена id={scheduled_shift_id} успешно удалена!",
            scheduled_shift_id=scheduled_shift.id,
        )
