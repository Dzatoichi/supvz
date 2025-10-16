from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
)


class SubEnum(Enum):
    paid = "paid"
    test = "test"
    expired = "expired"

class PVZType(Enum):
    wb = "wb"
    ozon = "ozon"
    yamarket = "yamarket"


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

