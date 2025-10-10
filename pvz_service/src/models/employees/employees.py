from typing import List

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.pvzs.PVZs import PVZs

employee_pvz_association = Table(
    "employee_pvz_association",
    Base.metadata,
    Column(
        "employee_id",
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "pvz_id",
        Integer,
        ForeignKey("pvz.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Employees(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(index=True, nullable=False)

    pvzs: Mapped[List["PVZs"]] = relationship(
        "PVZs",
        secondary=employee_pvz_association,  # таблица‑ассоциация
        back_populates="employees",
        lazy="selectin",  # fetch‑режим для async‑сессий
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, user_id={self.user_id}), owner_id={self.owner_id}>"
