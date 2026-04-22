from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.custom_positions_schemas import CustomPositionReadSchema
from src.schemas.enums import PositionSourceEnum


class SystemPositionBaseSchema(BaseModel):
    """Базовая схема системной должности."""

    title: str


class SystemPositionReadSchema(SystemPositionBaseSchema):
    """Схема для чтения системной должности."""

    id: int
    position_source: Literal[PositionSourceEnum.system] = PositionSourceEnum.system

    model_config = ConfigDict(from_attributes=True)


PositionReadSchema = Annotated[
    SystemPositionReadSchema | CustomPositionReadSchema,
    Field(discriminator="position_source"),
]
