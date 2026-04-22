from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    pass


class Permissions(Base):
    """Модель сущности права доступа."""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code_name: Mapped[str] = mapped_column(
        String(120),
        unique=True,
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    system_position_links: Mapped[List["SystemPositionPermissions"]] = relationship(
        "SystemPositionPermissions",
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    custom_position_links: Mapped[List["CustomPositionPermissions"]] = relationship(
        "CustomPositionPermissions",
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    user_links = relationship(
        "UserPermissions",
        back_populates="permission",
        cascade="all, delete-orphan",
    )
