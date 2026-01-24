from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class ShiftPenalty(Base):
    """Модель штрафа сотрудника."""

    __tablename__ = "shift_penalties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
        comment="ID сотрудника",
    )
    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Причина штрафа",
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
