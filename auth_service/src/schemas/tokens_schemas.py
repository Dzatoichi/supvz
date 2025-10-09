from enum import StrEnum


class TokenTypesEnum(StrEnum):
    """
    Перечисление типов токена.
    """

    access = "access"
    refresh = "refresh"
    register = "register"
