import re
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator

from src.schemas.pvz_schemas import PVZRead


class EmployeeCreateRequestSchema(BaseModel):
    """Схема запроса для создания нового сотрудника."""

    user_id: int
    owner_id: int

    name: str
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        """
        Функция валидации номера телефона.
        """
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError("Invalid phone number")
        return values

    model_config = ConfigDict(from_attributes=True)


class EmployeeResponseSchema(BaseModel):
    """Схема ответа, описывающая данные сотрудника и связанные ПВЗ."""

    user_id: int
    owner_id: int

    name: str
    phone_number: str

    pvzs: List[PVZRead]

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdateRequestSchema(BaseModel):
    """Схема запроса для обновления данных сотрудника."""

    name: str | None = None
    phone_number: str | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        """
        Функция валидации номера телефона.
        """
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError("Invalid phone number")
        return values

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class TransferRequestSchema(BaseModel):
    """Схема запроса для перевода сотрудника в другой ПВЗ."""

    new_pvz_id: int
