from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
)


class PVZType(Enum):
    wb = "wb"
    ozon = "ozon"
    yamarket = "yamarket"

class PVZBase(BaseModel):
    code: str
    type: PVZType
    group: str | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class PVZAdd(BaseModel):
    code: str
    type: PVZType
    address: str
    owner_id: int
    group: str | None = None
    curator_id: int | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class PVZUpdate(BaseModel):
    address: str
    owner_id: int
    curator_id: int | None = None
    group: str | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class PVZRead(PVZAdd):
    id: int
    created_at: datetime


class PVZGroup(BaseModel):
    group: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class PVZGet(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
