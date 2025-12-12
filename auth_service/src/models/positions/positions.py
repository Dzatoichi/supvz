from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.schemas.positions_schemas import PositionSourceEnum

if TYPE_CHECKING:
    from src.models.position_permissions.position_permissions import (
        CustomPositionPermissions,
        SystemPositionPermissions,
    )


class SystemPositions(Base):
    """Модель сущности должности."""

    __tablename__ = "system_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(255))

    permission_links: Mapped[List["SystemPositionPermissions"]] = relationship(
        "SystemPositionPermissions",
        back_populates="position",
        cascade="all, delete-orphan",
    )

    @property
    def position_source(self) -> str:
        return PositionSourceEnum.system


class CustomPositions(Base):
    """Модель сущности должности."""

    __tablename__ = "custom_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(255))

    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    permission_links: Mapped[List["CustomPositionPermissions"]] = relationship(
        "CustomPositionPermissions",
        back_populates="position",
        cascade="all, delete-orphan",
    )

    @property
    def position_source(self) -> str:
        return PositionSourceEnum.custom
