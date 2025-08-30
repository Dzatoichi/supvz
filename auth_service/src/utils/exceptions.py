# region Token Exceptions
class BaseTokenException(Exception):
    pass


class TokenExpiredException(BaseTokenException):
    pass


class InvalidTokenException(BaseTokenException):
    pass
