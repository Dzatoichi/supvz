from typing import Literal

from pydantic import BaseModel, ConfigDict

from src.schemas.enums import PositionSourceEnum


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
    permission_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)


class CustomPositionWithPermissionsReadSchema(CustomPositionBaseSchema):
    """Схема для чтения кастомной должности."""

    id: int
    permission_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)
