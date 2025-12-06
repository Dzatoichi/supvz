from pydantic import BaseModel, ConfigDict


class PositionBaseSchema(BaseModel):
    """Базовая схема для должности."""

    title: str
    owner_id: int


class PositionCreateSchema(PositionBaseSchema):
    """Схема для создания должности."""

    permissions: list[int] | None = None


class PositionReadSchema(PositionBaseSchema):
    """Схема для чтения должности."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class PositionUpdateSchema(BaseModel):
    """Схема для обновления должности."""

    title: str | None = None
    permissions_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)


class PositionWithPermissionsReadSchema(PositionBaseSchema):
    """Схема для чтения должности."""

    id: int
    permissions_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)
