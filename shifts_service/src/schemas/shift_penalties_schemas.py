from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PenaltyTypeEnum(str, Enum):
    """Типы штрафов для смен."""

    LATE_START = "late_start"
    EARLY_END = "early_end"
    MISS = "miss"
    OTHER = "other"


class ShiftPenaltyBaseSchema(BaseModel):
    """Базовая схема штрафа смены."""

    scheduled_shift_id: int
    type: PenaltyTypeEnum
    description: str
    penalty_minutes: int | None = None
    penalty_points: int = Field(default=0, ge=0)
    detected_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ShiftPenaltyCreateSchema(BaseModel):
    """Схема создания штрафа."""

    scheduled_shift_id: int
    type: PenaltyTypeEnum
    description: str = Field(..., min_length=1, max_length=1000)
    penalty_minutes: int | None = Field(default=None, ge=0, description="Количество минут опоздания/раннего ухода")
    penalty_points: int = Field(default=0, ge=0, description="Штрафные баллы")
    detected_at: datetime | None = None

    @field_validator("detected_at")
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    @field_validator("penalty_minutes")
    @classmethod
    def validate_penalty_minutes_for_type(cls, v: int | None, info) -> int | None:
        """Валидация минут штрафа в зависимости от типа."""
        penalty_type = info.data.get("type")
        if penalty_type in [PenaltyTypeEnum.LATE_START, PenaltyTypeEnum.EARLY_END]:
            if v is None:
                raise ValueError(f"penalty_minutes обязателен для типа {penalty_type}")
        return v


class ShiftPenaltyUpdateSchema(BaseModel):
    """Схема обновления штрафа."""

    type: PenaltyTypeEnum | None = None
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    penalty_minutes: int | None = Field(default=None, ge=0)
    penalty_points: int | None = Field(default=None, ge=0)
    detected_at: datetime | None = None

    @field_validator("detected_at")
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class ShiftPenaltyReadSchema(BaseModel):
    """Схема чтения штрафа."""

    id: int
    scheduled_shift_id: int
    type: PenaltyTypeEnum
    description: str
    penalty_minutes: int | None
    penalty_points: int
    detected_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShiftPenaltyFilterSchema(BaseModel):
    """Схема фильтрации штрафов."""

    scheduled_shift_id: int | None = None
    type: PenaltyTypeEnum | None = None
    penalty_points_min: int | None = Field(default=None, ge=0)
    penalty_points_max: int | None = Field(default=None, ge=0)
    detected_at_from: datetime | None = None
    detected_at_to: datetime | None = None
    created_at_from: datetime | None = None
    created_at_to: datetime | None = None

    @field_validator("detected_at_from", "detected_at_to", "created_at_from", "created_at_to")
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class ShiftPenaltySummarySchema(BaseModel):
    """Схема сводки штрафов по смене/сотруднику."""

    total_penalties: int = Field(description="Общее количество штрафов")
    total_points: int = Field(description="Общее количество штрафных баллов")
    late_start_count: int = Field(default=0, description="Количество опозданий")
    early_end_count: int = Field(default=0, description="Количество ранних уходов")
    miss_count: int = Field(default=0, description="Количество пропусков")
    other_count: int = Field(default=0, description="Количество других нарушений")
    total_late_minutes: int = Field(default=0, description="Общее время опозданий в минутах")

    model_config = ConfigDict(from_attributes=True)
