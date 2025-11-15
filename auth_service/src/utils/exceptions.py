class UserAlreadyExistsException(Exception):
    """Пользователь с таким логином/email уже существует."""

    pass


class WeakPasswordException(Exception):
    """Пароль не удовлетворяет требованиям безопасности."""

    pass


class InvalidEmailFormatException(Exception):
    """Email имеет неверный формат."""

    pass


class InvalidPhoneFormatException(Exception):
    """Телефон имеет неверный формат."""

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


class TokenNotProvidedException(Exception):
    """Токен не был передан в запросе."""

    pass


class RefreshTokenExpiredException(Exception):
    """Срок действия refresh-токена истёк."""

    pass


class PermissionDeniedException(Exception):
    """Недостаточно прав для выполнения действия."""

    pass


class ResetCodeInvalidException(Exception):
    """Неверный код сброса пароля."""

    pass


class ResetCodeExpiredException(Exception):
    """Код сброса пароля истёк."""

    pass
