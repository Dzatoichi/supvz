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


class PVZAdd(BaseModel):
    code: str
    type: PVZType
    address: str
    group_id: int | None = None
    responsible_id: int | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class PVZUpdate(BaseModel):
    address: str | None = None
    owner_id: int | None = None
    type: PVZType | None = None
    responsible_id: int | None = None
    group_id: int | None = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class PVZRead(PVZAdd):
    id: int
    created_at: datetime
