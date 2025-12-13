class UserAlreadyExistsException(Exception):
    """Пользователь с таким логином/email уже существует."""

    pass


class UserNotFoundException(Exception):
    """Пользователь не найден."""

    pass


class IncorrectPasswordException(Exception):
    """Неверный пароль."""

    pass


class TokenExpiredException(Exception):
    """
    Исключение для истёкших токенов.
    """

    pass


class InvalidTokenException(Exception):
    """
    Исключение для недействительных токенов.
    """

    pass


class PermissionDeniedException(Exception):
    """Недостаточно прав для выполнения действия."""

    pass


class PositionNotFoundException(Exception):
    """Должность не найдена."""

    pass


class PositionAlreadyExistsException(Exception):
    """Должность уже существует."""

    pass


class PermissionsNotFound(Exception):
    """Должность не найдена."""

    pass


class PermissionsFilterException(Exception):
    """Ошибка фильтрации при работе с permissions"""

    pass
