from pydantic import BaseModel, ConfigDict


class SystemPositionBaseSchema(BaseModel):
    """Базовая схема системной должности."""

    title: str


class SystemPositionReadSchema(SystemPositionBaseSchema):
    """Схема для чтения системной должности."""

    id: int

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
