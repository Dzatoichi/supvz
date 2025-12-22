from datetime import datetime

from sqlalchemy import CheckConstraint, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class ScheduledShifts(Base):
    """
    Табличка для смен,
    которые определяются заранее куратором,
    овнером или кто бы то ни был из главных ролей пвз.
    """

    __tablename__ = "scheduled_shifts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pvz_id: Mapped[int] = mapped_column(nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    starts_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    ends_at: Mapped[datetime] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="scheduled")
    paid: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("now()"))

    __table_args__ = (
        CheckConstraint("ends_at > starts_at", name="check_ends_after_starts"),
        CheckConstraint("status IN ('scheduled', 'completed', 'missed', 'cancelled')", name="check_valid_status"),
        Index("idx_user_starts", user_id, starts_at),
        Index("idx_pvz_starts", pvz_id, starts_at),
        Index("idx_status_starts", status, starts_at),
    )
