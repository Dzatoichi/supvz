from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PvzInEmployeeResponse(BaseModel):
    id: int
    address: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class EmployeeCreateRequest(BaseModel):
    user_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class EmployeeResponse(BaseModel):
    id: int
    user_id: int
    owner_id: int
    pvzs: List[PvzInEmployeeResponse]

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdateRequest(BaseModel):
    name: Optional[str] = None
    user_id: Optional[int] = None
    owner_id: Optional[int] = None


class TransferRequest(BaseModel):
    new_pvz_id: int
