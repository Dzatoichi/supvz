from typing import Optional

from pydantic import BaseModel, ConfigDict


class PVZGroupBase(BaseModel):
    """Базовая схема группы ПВЗ с общими полями."""

    name: str
    curator_id: Optional[int] = None


class PVZGroupCreateSchema(PVZGroupBase):
    """Схема для создания группы ПВЗ. Содержит обязательный owner_id."""

    owner_id: int


class PVZGroupUpdateSchema(PVZGroupBase):
    """Схема для обновления группы ПВЗ. Все поля опциональны."""

    pass


class PVZGroupResponseSchema(PVZGroupBase):
    """Схема ответа для группы ПВЗ с ID и owner_id."""

    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class AssignPVZToGroupSchema(BaseModel):
    """Схема для привязки ПВЗ к группе."""

    pvz_ids: list[int]


class DetailResponseSchema(BaseModel):
    """Схема для стандартного ответа с сообщением о результате операции."""

    detail: str
