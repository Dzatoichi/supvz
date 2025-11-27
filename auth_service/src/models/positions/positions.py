from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.models.permissions.permissions import Permissions


class Positions(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str | None] = mapped_column(String(255))

    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    permission_links: Mapped[List["PositionPermissions"]] = relationship(
        "PositionPermissions",
        back_populates="position",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class PositionPermissions(Base):
    __tablename__ = "positions_permissions"

    position_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("positions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    permission_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    position: Mapped["Positions"] = relationship(
        "Positions",
        back_populates="permission_links",
        lazy="selectin",
    )
    permission: Mapped["Permissions"] = relationship(
        "Permissions",
        back_populates="position_links",
        lazy="selectin",
    )
