from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class PositionSourceEnum(str, Enum):
    """Перечисление таблиц с должностями"""

    system = "system"
    custom = "custom"


class SystemPositionBaseSchema(BaseModel):
    """Базовая схема системной должности."""

    title: str


class SystemPositionReadSchema(SystemPositionBaseSchema):
    """Схема для чтения системной должности."""

    id: int
    position_source: Literal[PositionSourceEnum.system] = PositionSourceEnum.system

    model_config = ConfigDict(from_attributes=True)


class CustomPositionBaseSchema(BaseModel):
    """Базовая схема кастомной должности."""

    title: str
    owner_id: int


class CustomPositionCreateSchema(CustomPositionBaseSchema):
    """Создание кастомной должности."""

    permission_ids: list[int] | None = None


class CustomPositionReadSchema(CustomPositionBaseSchema):
    """Схема для чтения кастомной должности."""

    id: int
    position_source: Literal[PositionSourceEnum.custom] = PositionSourceEnum.custom

    model_config = ConfigDict(from_attributes=True)


class CustomPositionUpdateSchema(BaseModel):
    """Схема для обновления кастомной должности."""

    title: str | None = None
    permissions_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)


class CustomPositionWithPermissionsReadSchema(CustomPositionBaseSchema):
    """Схема для чтения кастомной должности."""

    id: int
    permissions_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)


PositionReadSchema = Annotated[
    SystemPositionReadSchema | CustomPositionReadSchema,
    Field(discriminator="position_source"),
]
