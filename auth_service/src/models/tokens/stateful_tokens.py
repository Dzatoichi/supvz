from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.users.users import Users


class StatefulTokens(Base):
    __tablename__ = "stateful_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('users.id', ondelete="CASCADE"),
                                         nullable=False,
                                         index=True)
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="stateful_tokens",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<StatefulTokens(id={self.id}, user_id={self.user_id}, used={self.used})>"
