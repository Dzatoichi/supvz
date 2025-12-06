from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class SystemPositionPermissions(Base):
    __tablename__ = "system_position_permissions"

    system_position_id: Mapped[int] = mapped_column(
        ForeignKey("system_positions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    position = relationship("SystemPositions", back_populates="permission_links")
    permission = relationship("Permissions", back_populates="system_role_links")


class CustomPositionPermissions(Base):
    __tablename__ = "custom_position_permissions"

    custom_position_id: Mapped[int] = mapped_column(
        ForeignKey("custom_positions.id", ondelete="CASCADE"), primary_key=True
    )

    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)

    position = relationship("CustomPositions", back_populates="permission_links")
    permission = relationship("Permissions", back_populates="custom_role_links")
