from enum import Enum


class PositionSourceEnum(str, Enum):
    """Перечисление таблиц с должностями"""

    system = "system"
    custom = "custom"
