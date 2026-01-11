from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ShiftBaseSchema(BaseModel):
    """Базовая схема смены."""

    scheduled_shift_id: int
    started_at: datetime | None = None
    ended_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ShiftCreateSchema(BaseModel):
    """Схема создания смены."""

    scheduled_shift_id: int
    started_at: datetime | None = None
    ended_at: datetime | None = None

    @field_validator("started_at", "ended_at")
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    @field_validator("ended_at")
    @classmethod
    def validate_ended_at(cls, v: datetime | None, info) -> datetime | None:
        """Проверяет, что ended_at больше started_at."""
        if v is not None and info.data.get("started_at") is not None:
            if v <= info.data["started_at"]:
                raise ValueError("ended_at must be greater than started_at")
        return v


class ShiftUpdateSchema(BaseModel):
    """Схема обновления смены."""

    scheduled_shift_id: int | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None

    @field_validator("started_at", "ended_at")
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    @field_validator("ended_at")
    @classmethod
    def validate_ended_at(cls, v: datetime | None, info) -> datetime | None:
        """Проверяет, что ended_at больше started_at."""
        if v is not None and info.data.get("started_at") is not None:
            if v <= info.data["started_at"]:
                raise ValueError("ended_at must be greater than started_at")
        return v


class ShiftReadSchema(BaseModel):
    """Схема чтения смены."""

    id: int
    scheduled_shift_id: int
    started_at: datetime
    ended_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ShiftFilterSchema(BaseModel):
    """Схема фильтрации смен."""

    scheduled_shift_id: int | None = None
    started_at_from: datetime | None = None
    started_at_to: datetime | None = None
    ended_at_from: datetime | None = None
    ended_at_to: datetime | None = None
    is_active: bool | None = None

    @field_validator("started_at_from", "started_at_to", "ended_at_from", "ended_at_to")
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v
