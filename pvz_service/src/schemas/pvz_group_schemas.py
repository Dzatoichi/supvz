from typing import Optional

from pydantic import BaseModel, ConfigDict


class PVZGroupBase(BaseModel):
    """Базовая схема группы ПВЗ с общими полями."""

    name: str
    curator_id: Optional[int] = None


class PVZGroupCreate(PVZGroupBase):
    """Схема для создания группы ПВЗ. Содержит обязательный owner_id."""

    owner_id: int


class PVZGroupUpdate(PVZGroupBase):
    """Схема для обновления группы ПВЗ. Все поля опциональны."""

    pass


class PVZGroupResponse(PVZGroupBase):
    """Схема ответа для группы ПВЗ с ID и owner_id."""

    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
