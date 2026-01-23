from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from src.enums.inbox import EventStatus, EventType


class InboxBaseSchema(BaseModel):
    """Базовые поля, обязательные для всех операций"""

    event_id: str
    event_type: EventType


class InboxCreateSchema(InboxBaseSchema):
    """
    Схема для создания новой записи в Inbox.
    """

    payload: dict[str, Any]


class InboxReadSchema(InboxBaseSchema):
    """
    Схема для чтения записи из БД (возврат из DAO).
    Полное отражение модели SQLAlchemy.
    """

    status: EventStatus
    payload: dict[str, Any]
    response_body: Optional[dict[str, Any]] = None
    created_at: datetime
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class InboxUpdateSchema(BaseModel):
    """
    Схема для обновления записи.
    """

    status: EventStatus
    response_body: Optional[dict[str, Any]] = None
    finished_at: Optional[datetime] = None
