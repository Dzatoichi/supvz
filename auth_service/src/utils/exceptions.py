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
