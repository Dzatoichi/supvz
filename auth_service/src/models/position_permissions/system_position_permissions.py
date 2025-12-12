from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class SystemPositionPermissions(Base):
    """Таблица ассоциаций системных должностей с правами доступа."""

    __tablename__ = "system_position_permissions"

    system_position_id: Mapped[int] = mapped_column(
        ForeignKey("system_positions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    position: Mapped["SystemPositions"] = relationship(
        "SystemPositions",
        back_populates="permission_links",
    )

    permission: Mapped["Permissions"] = relationship(
        "Permissions",
        back_populates="system_position_links",
    )
