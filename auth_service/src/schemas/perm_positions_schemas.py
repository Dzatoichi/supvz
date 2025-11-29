from pydantic import BaseModel, ConfigDict


class PermissionBaseSchema(BaseModel):
    code_name: str
    description: str | None = None


class PermissionCreateSchema(PermissionBaseSchema):
    pass


class PermissionReadSchema(PermissionBaseSchema):
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
    permissions: list[PermissionReadSchema] | None = []


class PositionUpdateSchema(BaseModel):
    title: str | None = None
    permissions_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)
