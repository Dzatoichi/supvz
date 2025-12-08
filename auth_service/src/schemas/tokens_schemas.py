from enum import StrEnum


class TokenTypesEnum(StrEnum):
    """
    Перечисление типов токенов.
    """

    access = "access"
    refresh = "refresh"
    register = "register"
