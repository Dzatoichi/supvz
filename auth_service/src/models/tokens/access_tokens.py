from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from auth_service.src.database.base import Base

if TYPE_CHECKING:
    from auth_service.src.models.users.users import Users

class AccessTokens(Base):
    __tablename__ = "access_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="access_tokens",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<AccessToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"
