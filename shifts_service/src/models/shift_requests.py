from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.schemas.shift_requests_schemas import RequestStatusEnum


class ShiftRequest(Base):
    """Модель запроса на смену."""

    __tablename__ = "shift_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scheduled_shift_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )
    request_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    new_user_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=RequestStatusEnum.PENDING.value,
    )
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    processed_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    scheduled_shift_start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
