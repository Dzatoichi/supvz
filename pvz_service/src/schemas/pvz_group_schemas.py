from typing import Optional

from pydantic import BaseModel, ConfigDict


class PVZGroupBaseSchema(BaseModel):
    """Базовая схема группы ПВЗ с общими полями."""

    name: str
    curator_id: Optional[int] = None


class PVZGroupCreateSchema(PVZGroupBaseSchema):
    """Схема для создания группы ПВЗ. Содержит обязательный owner_id."""

    owner_id: int


class PVZGroupUpdateSchema(PVZGroupBaseSchema):
    """Схема для обновления группы ПВЗ. Все поля опциональны."""

    pass


class PVZGroupResponseSchema(PVZGroupBaseSchema):
    """Схема ответа для группы ПВЗ с ID и owner_id."""

    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class PVZAssignmentSchema(BaseModel):
    """Схема для привязки ПВЗ к группе."""

    group_id: int
    pvz_ids: list[int]


class DetailResponseSchema(BaseModel):
    """Схема для стандартного ответа с сообщением о результате операции."""

    detail: str
