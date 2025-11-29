from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi_pagination import Page, paginate
from fastapi_pagination.params import Params

from src.schemas.scheduled_shifts_schemas import (
    ScheduledShiftCreateSchema,
    ScheduledShiftReadSchema,
    ScheduledShiftUpdateSchema,
)


class FakeScheduledShiftsService:
    """
    Фейковый сервис для тестирования API ручек ScheduledShifts.
    """

    _fake_db = [
        ScheduledShiftReadSchema(
            id=1,
            pvz_id=1,
            user_id=1,
            starts_at=datetime.now() + timedelta(days=1),
            ends_at=datetime.now() + timedelta(days=1, hours=8),
            completed=False,
            status="scheduled",
            paid=False,
        ),
        ScheduledShiftReadSchema(
            id=2,
            pvz_id=2,
            user_id=2,
            starts_at=datetime.now() + timedelta(days=2),
            ends_at=datetime.now() + timedelta(days=2, hours=8),
            completed=True,
            status="completed",
            paid=True,
        ),
        ScheduledShiftReadSchema(
            id=3,
            pvz_id=1,
            user_id=3,
            starts_at=datetime.now() + timedelta(days=3),
            ends_at=datetime.now() + timedelta(days=3, hours=8),
            completed=False,
            status="scheduled",
            paid=False,
        ),
    ]

    async def create_scheduled_shift(
        self, scheduled_shift_data: ScheduledShiftCreateSchema, repo
    ) -> ScheduledShiftReadSchema:
        if scheduled_shift_data.ends_at <= scheduled_shift_data.starts_at:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="End time must be after start time",
            )

        new_id = max(shift.id for shift in self._fake_db) + 1 if self._fake_db else 1
        new_shift = ScheduledShiftReadSchema(
            id=new_id,
            **scheduled_shift_data.model_dump(),
            completed=False,
            status="scheduled",
            paid=False,
        )

        self._fake_db.append(new_shift)
        return new_shift

    async def get_scheduled_shifts(
        self,
        user_id: Optional[int] = None,
        pvz_id: Optional[int] = None,
        starts_at: Optional[datetime] = None,
        ends_at: Optional[datetime] = None,
        completed: Optional[bool] = None,
        status: Optional[str] = None,
        paid: Optional[bool] = None,
        repo=None,
        params: Params = None,
    ) -> Page[ScheduledShiftReadSchema]:
        results = self._fake_db

        if user_id is not None:
            results = [shift for shift in results if shift.user_id == user_id]
        if pvz_id is not None:
            results = [shift for shift in results if shift.pvz_id == pvz_id]
        if starts_at is not None:
            results = [shift for shift in results if shift.starts_at >= starts_at]
        if ends_at is not None:
            results = [shift for shift in results if shift.ends_at <= ends_at]
        if completed is not None:
            results = [shift for shift in results if shift.completed == completed]
        if status is not None:
            results = [shift for shift in results if shift.status == status]
        if paid is not None:
            results = [shift for shift in results if shift.paid == paid]

        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Смены не найдены",
            )

        return paginate(results, params)

    async def get_scheduled_shift_by_id(self, scheduled_shift_id: int, repo) -> ScheduledShiftReadSchema:
        for shift in self._fake_db:
            if shift.id == scheduled_shift_id:
                return shift

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled shift not found",
        )

    async def update_scheduled_shift(
        self, scheduled_shift_id: int, updated_data: ScheduledShiftUpdateSchema, repo
    ) -> ScheduledShiftReadSchema:
        for i, shift in enumerate(self._fake_db):
            if shift.id == scheduled_shift_id:
                update_dict = updated_data.model_dump(exclude_unset=True)

                if "status" in update_dict and update_dict["status"] not in ["scheduled", "completed", "missed"]:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Invalid status value",
                    )

                if "starts_at" in update_dict or "ends_at" in update_dict:
                    new_starts_at = update_dict.get("starts_at", shift.starts_at)
                    new_ends_at = update_dict.get("ends_at", shift.ends_at)
                    if new_ends_at <= new_starts_at:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="End time must be after start time",
                        )

                for key, value in update_dict.items():
                    setattr(self._fake_db[i], key, value)

                return self._fake_db[i]

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled shift not found",
        )

    async def delete_scheduled_shift(self, scheduled_shift_id: int, repo) -> None:
        for i, shift in enumerate(self._fake_db):
            if shift.id == scheduled_shift_id:
                self._fake_db.pop(i)
                return

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled shift not found",
        )
