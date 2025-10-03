from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    StringConstraints,
    field_validator,
    model_validator,
)

class PVZType(Enum):
    wb = "wb"
    ozon = "ozon"
    yamarket = "yamarket"

class PVZBase(BaseModel):
    code: int
    type: PVZType
    address: str
    group: str
    owner_id: int
    curator_id: int

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
