from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.schemas.users_schemas import SubEnum, UserRole

if TYPE_CHECKING:
    from src.models.tokens.refresh_tokens import RefreshTokens


class Users(Base):
    """
    Класс модели-сущности пользователя.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    phone_number: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(
            UserRole,
            name="user_role",
            native_enum=False,
        ),
        nullable=False,
        default=UserRole.owner,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    refresh_tokens: Mapped[List["RefreshTokens"]] = relationship(
        "RefreshTokens",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    subscription: Mapped[SubEnum] = mapped_column(
        SAEnum(
            SubEnum,
            name="subscription",
            native_enum=False,
        ),
        nullable=True,
        default=SubEnum.test,
    )

    def __repr__(self) -> str:
        """
        Метод возвращения пользователя в виде строки.
        """
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
