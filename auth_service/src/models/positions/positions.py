from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.models.position_permissions.position_permissions import PositionPermissions


class Positions(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(255))

    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    permission_links: Mapped[List["PositionPermissions"]] = relationship(
        "PositionPermissions",
        back_populates="position",
        cascade="all, delete-orphan",
    )
