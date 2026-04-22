from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.models.permissions.permissions import Permissions
    from src.models.users.users import Users


class UserPermissions(Base):
    """Ассоциация пользователя и права доступа."""

    __tablename__ = "user_permissions"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="permission_links",
    )
    permission: Mapped["Permissions"] = relationship(
        "Permissions",
        back_populates="user_links",
    )
