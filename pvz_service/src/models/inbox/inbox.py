from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.enums.inbox import EventStatus, EventType


class InboxEvents(Base):
    __tablename__ = "inbox"

    # Композитный индекс для очистки старых записей и поиска stale событий
    __table_args__ = (Index("ix_inbox_status_created_at", "status", "created_at"),)

    event_id: Mapped[str] = mapped_column(String, primary_key=True)

    event_type: Mapped[EventType] = mapped_column(SAEnum(EventType), nullable=False)

    status: Mapped[EventStatus] = mapped_column(
        SAEnum(EventStatus),
        default=EventStatus.PROCESSING,
        server_default=EventStatus.PROCESSING.name,
        nullable=False,
    )

    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    response_body: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    error_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
