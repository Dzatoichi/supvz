from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


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
    )
    permission: Mapped["Permissions"] = relationship(
        "Permissions",
        back_populates="position_links",
    )
