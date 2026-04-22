from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.models.users.users import Users


class RefreshTokens(Base):
    """
    Класс модели-сущности refresh-токена.
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="refresh_tokens",
        lazy="joined",
    )

    def __repr__(self) -> str:
        """
        Метод возвращения refresh-токена в виде строки.
        """
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked}), expires_at={self.expires_at})>"
