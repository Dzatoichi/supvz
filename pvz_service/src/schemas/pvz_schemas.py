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
    group: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class PVZGroup(BaseModel):
    id: int
    group: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

