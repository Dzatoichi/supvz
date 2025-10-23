import re
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class PvzInEmployeeResponseSchema(BaseModel):
    """Схема вложенного объекта ПВЗ, используемая в ответе при возврате данных о сотруднике."""

    id: int
    address: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class EmployeeCreateRequestSchema(BaseModel):
    """Схема запроса для создания нового сотрудника."""

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
    """Схема ответа, описывающая данные сотрудника и связанные ПВЗ."""

    user_id: int
    owner_id: int

    name: str | None = None
    phone_number: str | None = None

    pvzs: List[PvzInEmployeeResponseSchema]

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdateRequestSchema(BaseModel):
    """Схема запроса для обновления данных сотрудника."""

    name: Optional[str] = None
    phone_number: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        """
        Функция валиадации номера телефона.
        """
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError("Invalid phone number")
        return values

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class TransferRequestSchema(BaseModel):
    """Схема запроса для перевода сотрудника в другой ПВЗ."""

    new_pvz_id: int
