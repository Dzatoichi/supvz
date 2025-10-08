from pydantic import BaseModel


class TransferRequest(BaseModel):
    new_pvz_id: int
