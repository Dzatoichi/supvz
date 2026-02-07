from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SalaryRuleType(str, Enum):
    """Типы правил расчета зарплаты."""

    HOURLY = "hourly"
    PER_SHIFT = "per_shift"
    FIXED = "fixed"
    MIXED = "mixed"


class SalaryRuleBaseSchema(BaseModel):
    """Базовая схема правила расчета зарплаты."""

    name: str = Field(..., min_length=1, max_length=100, description="Название правила")
    rule_type: SalaryRuleType = Field(..., description="Тип правила расчета")
    rate: float = Field(..., gt=0, description="Ставка")
    overtime_multiplier: float | None = Field(default=1.5, ge=1.0, description="Множитель за сверхурочные")
    night_multiplier: float | None = Field(default=1.25, ge=1.0, description="Множитель за ночные часы")
    holiday_multiplier: float | None = Field(default=2.0, ge=1.0, description="Множитель за праздничные дни")
    is_active: bool = Field(default=True, description="Активно ли правило")

    model_config = ConfigDict(from_attributes=True)

    @field_validator("rate")
    @classmethod
    def validate_rate(cls, v: float) -> float:
        """Проверяет корректность ставки."""
        if v <= 0:
            raise ValueError("Ставка должна быть положительным числом")
        return v


class SalaryRuleCreateSchema(BaseModel):
    """Схема создания правила расчета зарплаты."""

    pvz_id: int = Field(..., description="ID пункта выдачи заказов")
    name: str = Field(..., min_length=1, max_length=100, description="Название правила")
    rule_type: SalaryRuleType = Field(..., description="Тип правила расчета")
    rate: float = Field(..., gt=0, description="Ставка")
    overtime_multiplier: float | None = Field(default=1.5, ge=1.0, description="Множитель за сверхурочные")
    night_multiplier: float | None = Field(default=1.25, ge=1.0, description="Множитель за ночные часы")
    holiday_multiplier: float | None = Field(default=2.0, ge=1.0, description="Множитель за праздничные дни")
    is_active: bool = Field(default=True, description="Активно ли правило")


class SalaryRuleUpdateSchema(BaseModel):
    """Схема обновления правила расчета зарплаты."""

    name: str | None = Field(default=None, min_length=1, max_length=100, description="Название правила")
    rule_type: SalaryRuleType | None = Field(default=None, description="Тип правила расчета")
    rate: float | None = Field(default=None, gt=0, description="Ставка")
    overtime_multiplier: float | None = Field(default=None, ge=1.0, description="Множитель за сверхурочные")
    night_multiplier: float | None = Field(default=None, ge=1.0, description="Множитель за ночные часы")
    holiday_multiplier: float | None = Field(default=None, ge=1.0, description="Множитель за праздничные дни")
    is_active: bool | None = Field(default=None, description="Активно ли правило")


class SalaryRuleReadSchema(BaseModel):
    """Схема чтения правила расчета зарплаты."""

    id: int
    pvz_id: int
    name: str
    rule_type: SalaryRuleType
    rate: float
    overtime_multiplier: float | None
    night_multiplier: float | None
    holiday_multiplier: float | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SalaryRuleFilterSchema(BaseModel):
    """Схема фильтрации правил расчета зарплаты."""

    pvz_id: int | None = Field(default=None, description="ID пункта выдачи заказов")
    rule_type: SalaryRuleType | None = Field(default=None, description="Тип правила расчета")
    is_active: bool | None = Field(default=None, description="Активно ли правило")
