import re
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class PvzInEmployeeResponseSchema(BaseModel):
    id: int
    address: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class EmployeeCreateRequestSchema(BaseModel):
    user_id: int
    owner_id: int

    name: str | None = None
    phone_number: str | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        """
        Функция валиадации номера телефона.
        """
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError("Invalid phone number")
        return values

    model_config = ConfigDict(from_attributes=True)


class EmployeeResponseSchema(BaseModel):
    id: int
    user_id: int
    owner_id: int

    name: str | None = None
    phone_number: str | None = None

    pvzs: List[PvzInEmployeeResponseSchema]

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdateRequestSchema(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None

    user_id: Optional[int] = None
    owner_id: Optional[int] = None


class TransferRequestSchema(BaseModel):
    new_pvz_id: int
