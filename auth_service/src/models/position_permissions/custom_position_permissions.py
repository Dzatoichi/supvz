from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class CustomPositionPermissions(Base):
    """Таблица ассоциаций кастомных должностей с правами доступа."""

    __tablename__ = "custom_position_permissions"

    custom_position_id: Mapped[int] = mapped_column(
        ForeignKey("custom_positions.id", ondelete="CASCADE"), primary_key=True
    )

    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)

    position: Mapped["CustomPositions"] = relationship(
        "CustomPositions",
        back_populates="permission_links",
    )

    permission: Mapped["Permissions"] = relationship(
        "Permissions",
        back_populates="custom_position_links",
    )
