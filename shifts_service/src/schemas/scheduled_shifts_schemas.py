from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ScheduledShiftBaseSchema(BaseModel):
    """
    Базовая схема смены с валидацией дат ее начала и конца
    """

    starts_at: datetime
    ends_at: datetime

    @field_validator("ends_at")
    @classmethod
    def validate_dates(cls, ends_at: datetime, info):
        starts_at = info.data.get("starts_at")
        if starts_at and ends_at < starts_at:
            raise ValueError("дата ends_at должна быть позже starts_at")
        return ends_at

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class ScheduledShiftCreateSchema(ScheduledShiftBaseSchema):
    """
    Схема создания запланированной смены
    """

    pvz_id: int
    user_id: int


class ScheduledShiftReadSchema(ScheduledShiftCreateSchema):
    """
    Схема получения запланированных смен
    """

    id: int
    completed: bool
    status: str
    paid: bool


class ScheduledShiftUpdateSchema(ScheduledShiftBaseSchema):
    """
    Схема обновления запланированной смены
    """

    pvz_id: int | None = None
    user_id: int | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    completed: bool | None = None
    status: str | None = None
    paid: bool | None = None
