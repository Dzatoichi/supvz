import enum
from typing import List

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

employee_pvz_association = Table(
    "employee_pvz_association",
    Base.metadata,
    Column(
        "employee_id",
        Integer,
        ForeignKey("employees.user_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "pvz_id",
        Integer,
        ForeignKey("pvzs.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class PositionSourceEnum(str, enum.Enum):
    """Перечисление таблиц с должностями"""

    system = "system"
    custom = "custom"


class Employees(Base):
    """Модель сотрудника."""

    __tablename__ = "employees"

    user_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(index=True, nullable=False)
    position_id: Mapped[int] = mapped_column(nullable=False)
    position_source: Mapped[PositionSourceEnum] = mapped_column(
        Enum(PositionSourceEnum, native_enum=False),
        nullable=False,
        default=PositionSourceEnum.system,
    )

    pvzs: Mapped[List["PVZs"]] = relationship(
        "PVZs",
        secondary=employee_pvz_association,  # таблица‑ассоциация
        back_populates="employees",
        lazy="selectin",  # fetch‑режим для async‑сессий
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"<Employee(user={self.user_id}, owner_id={self.owner_id}>"
