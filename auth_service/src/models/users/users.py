from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.schemas.users_schemas import SubscriptionEnum

if TYPE_CHECKING:
    from src.models.permissions.permissions import Permissions
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

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

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
    subscription: Mapped[SubscriptionEnum] = mapped_column(
        SAEnum(
            SubscriptionEnum,
            name="subscription",
            native_enum=False,
        ),
        nullable=True,
        default=SubscriptionEnum.test,
    )

    permission_links: Mapped[List["UserPermissions"]] = relationship(
        "UserPermissions",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def permissions(self) -> List["Permissions"]:
        """Получить только личные permissions пользователя"""
        return [link.permission for link in self.permission_links]

    def __repr__(self) -> str:
        """
        Метод возвращения пользователя в виде строки.
        """
        return f"<User(id={self.id}, email={self.email}>"


class UserPermissions(Base):
    __tablename__ = "user_permissions"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="permission_links",
        lazy="selectin",
    )
    permission: Mapped["Permissions"] = relationship(
        "Permissions",
        back_populates="user_links",
        lazy="selectin",
    )
