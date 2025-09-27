from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class PVZs(Base):
    __tablename__ = "pvz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    group: Mapped[Optional[str]] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, index=True)
    curator_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<PVZs(id={self.id}, code={self.code})>"
