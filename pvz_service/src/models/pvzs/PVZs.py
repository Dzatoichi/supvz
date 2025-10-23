from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.pvzs.PVZGroups import PVZGroups
from src.schemas.pvz_schemas import PVZType


class PVZs(Base):
    __tablename__ = "pvzs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    type: Mapped[PVZType] = mapped_column(
        SAEnum(
            PVZType,
            name="pvz-type",
            native_enum=False,
        ),
        nullable=False,
    )
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    group_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("pvz_groups.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    owner_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, index=True)
    curator_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    group: Mapped[Optional["PVZGroups"]] = relationship("PVZGroups", back_populates="pvzs")

    def __repr__(self) -> str:
        return f"<PVZs(id={self.id}, code={self.code})>"
