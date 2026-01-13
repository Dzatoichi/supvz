from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class ShiftPenalty(Base):
    """Модель штрафа за смену."""

    __tablename__ = "shift_penalties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scheduled_shift_id: Mapped[int] = mapped_column(
        Integer,
        # ForeignKey("scheduled_shifts.id", ondelete="CASCADE"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    penalty_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Количество минут опоздания/раннего ухода",
    )
    penalty_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Штрафные баллы",
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
