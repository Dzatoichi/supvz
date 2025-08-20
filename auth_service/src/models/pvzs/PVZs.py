from __future__ import annotations
from typing import List, Optional
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from auth_service.src.models.users.users import Users


class PVZs(Base):
    __tablename__ = "pvzs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    owner_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    curator_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner: Mapped[Optional["Users"]] = relationship(
        "User",
        back_populates="pvz_owned",
        foreign_keys=[owner_id],
        lazy="joined"
    )

    curator: Mapped[Optional["Users"]] = relationship(
        "User",
        back_populates="pvz_curated",
        foreign_keys=[curator_id],
        lazy="joined"
    )

    worker_links: Mapped[List["PVZWorker"]] = relationship(
        "PVZWorker",
        back_populates="pvz",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<PVZ(id={self.id}, code={self.code})>"
