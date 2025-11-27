from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.models.positions.positions import PositionPermissions
    from src.models.users.users import UserPermissions


class Permissions(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code_name: Mapped[str] = mapped_column(
        String(120),
        unique=True,
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    position_links: Mapped[List["PositionPermissions"]] = relationship(
        "PositionPermissions",
        back_populates="permission",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    user_links: Mapped[List["UserPermissions"]] = relationship(
        "UserPermissions",
        back_populates="permission",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
