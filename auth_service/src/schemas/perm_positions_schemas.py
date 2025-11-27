from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    code_name: str
    description: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PositionBaseSchema(BaseModel):
    title: str
    owner_id: int


class PositionCreateSchema(PositionBaseSchema):
    permissions: list[int] | None = None


class PositionReadSchema(PositionBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PositionReadPermissionsSchema(PositionReadSchema):
    permissions: list[PermissionRead] | None = []
