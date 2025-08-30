from typing import List, Optional, TYPE_CHECKING
from enum import Enum as PyEnum
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from auth_service.src.database.base import Base

if TYPE_CHECKING:
    from auth_service.src.models.tokens.access_tokens import AccessTokens
    from auth_service.src.models.tokens.refresh_tokens import RefreshTokens
    from auth_service.src.models.pvzs.PVZ_workers import PVZWorkers
    from auth_service.src.models.pvzs.PVZs import PVZs


class UsersRoleEnum(str, PyEnum):
    OWNER = "owner"
    CURATOR = "curator"
    EMPLOYEE = "employee"

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UsersRoleEnum] = mapped_column(SAEnum(UsersRoleEnum, name="user_role", native_enum=False), nullable=False, default=UsersRoleEnum.EMPLOYEE)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    refresh_tokens: Mapped[List["RefreshTokens"]] = relationship(
        "RefreshTokens",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    access_tokens: Mapped[List["AccessTokens"]] = relationship(
        "AccessTokens",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    pvz_owned: Mapped[List["PVZs"]] = relationship(
        "PVZs",
        back_populates="owner",
        foreign_keys="[PVZs.owner_id]",
        lazy="selectin"
    )

    pvz_curated: Mapped[List["PVZs"]] = relationship(
        "PVZs",
        back_populates="curator",
        foreign_keys="[PVZs.curator_id]",
        lazy="selectin"
    )

    pvz_worker_links: Mapped[List["PVZWorkers"]] = relationship(
        "PVZWorkers",
        back_populates="worker",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
