from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.schemas.salary_schemas import SalaryRuleType


class SalaryRule(Base):
    """Модель правила расчета зарплаты."""

    __tablename__ = "salary_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pvz_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="ID пункта выдачи заказов")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Название правила")
    rule_type: Mapped[SalaryRuleType] = mapped_column(
        Enum(SalaryRuleType),
        nullable=False,
        comment="Тип правила расчета",
    )
    rate: Mapped[float] = mapped_column(Float, nullable=False, comment="Ставка (за час/смену/фиксированная)")
    overtime_multiplier: Mapped[float] = mapped_column(Float, nullable=True, comment="Множитель за сверхурочные")
    night_multiplier: Mapped[float] = mapped_column(Float, nullable=True, comment="Множитель за ночные часы")
    holiday_multiplier: Mapped[float] = mapped_column(Float, nullable=True, comment="Множитель за праздничные дни")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Активно ли правило")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<SalaryRule(id={self.id}, pvz_id={self.pvz_id}, name='{self.name}')>"
