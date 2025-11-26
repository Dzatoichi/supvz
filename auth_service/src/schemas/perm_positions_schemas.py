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
    name: str
    owner_id: int


class PositionCreateSchema(PositionBaseSchema):
    pass


class PositionReadSchema(PositionBaseSchema):
    id: int
    permissions: list[PermissionRead] = []

    model_config = ConfigDict(from_attributes=True)
