from pydantic import BaseModel, ConfigDict


class PermissionBaseSchema(BaseModel):
    """Базовая схема для прав доступа."""

    code_name: str
    description: str | None = None


class PermissionReadSchema(PermissionBaseSchema):
    """Схема для чтения права доступа."""

    id: int

    model_config = ConfigDict(from_attributes=True)
