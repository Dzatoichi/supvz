from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PenaltyBaseSchema(BaseModel):
    """Базовая схема штрафа."""

    employee_id: int = Field(..., description="ID сотрудника")
    reason: str = Field(..., min_length=1, max_length=2000, description="Причина штрафа")

    model_config = ConfigDict(from_attributes=True)


class PenaltyCreateSchema(BaseModel):
    """Схема создания штрафа."""

    employee_id: int = Field(..., description="ID сотрудника")
    reason: str = Field(..., min_length=1, max_length=2000, description="Причина штрафа")


class PenaltyUpdateSchema(BaseModel):
    """Схема обновления штрафа."""

    reason: str | None = Field(default=None, min_length=1, max_length=2000, description="Причина штрафа")


class PenaltyReadSchema(BaseModel):
    """Схема чтения штрафа."""

    id: int
    employee_id: int
    reason: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PenaltyFilterSchema(BaseModel):
    """Схема фильтрации штрафов."""

    employee_id: int | None = Field(default=None, description="ID сотрудника")
    created_at_from: datetime | None = Field(default=None, description="Дата создания от")
    created_at_to: datetime | None = Field(default=None, description="Дата создания до")

    @field_validator("created_at_from", "created_at_to")
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class PenaltySummarySchema(BaseModel):
    """Схема сводки штрафов по сотруднику."""

    total_penalties: int = Field(description="Общее количество штрафов")

    model_config = ConfigDict(from_attributes=True)
