from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.src.database.base import Base

if TYPE_CHECKING:
    from auth_service.src.models.pvzs.PVZs import PVZs
    from auth_service.src.models.users.users import Users


class PVZWorkers(Base):
    __tablename__ = "pvz_workers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pvz_id: Mapped[int] = mapped_column(Integer, ForeignKey('pvzs.id'), nullable=False, index=True)
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    pvz: Mapped["PVZs"] = relationship(
        "PVZ",
        back_populates="worker_links",
        lazy="joined"
    )

    worker: Mapped["Users"] = relationship(
        "User",
        back_populates="pvz_worker_links",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<PVZWorker(id={self.id}, pvz_id={self.pvz_id}, worker_id={self.worker_id})>"
