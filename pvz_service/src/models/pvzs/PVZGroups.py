from typing import List, Optional

from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class PVZGroups(Base):
    """Модель для групп ПВЗ."""

    __tablename__ = "pvz_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    curator_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )

    pvzs: Mapped[List["PVZs"]] = relationship(
        "PVZs",
        back_populates="group",
        cascade="all, delete-orphan",
    )

    __table_args__ = (UniqueConstraint("name", "owner_id", name="uq_pvz_groups_name_owner"),)

    def __repr__(self) -> str:
        return f"<PVZGroup(id={self.id}, name={self.name})>"
