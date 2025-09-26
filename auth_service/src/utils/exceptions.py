from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


def setup_exception_handlers(app: FastAPI):
    """
    Функция настройки глобальных обработчиков исключений для приложения.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Функция обработчика стандартных HTTP-исключений.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "http_error", "detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Функция обработчика ошибок валидации входящих данных.
        """
        errors = exc.errors()
        details = []
        for err in errors:
            if err.get("type") == "string_too_short":
                details.append(str(err.get("loc")[1]) + " " + str(err.get("msg")).lower())
            else:
                details.append(str(err.get("msg")))
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "validation_error", "detail": details},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """
        Функция обработчика ошибок SQLAlchemy.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "database_error", "detail": "DB operation failed"},
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "invalid_token", "detail": str(exc)},
        )

    @app.exception_handler(TokenExpiredException)
    async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "token_expired", "detail": str(exc)},
        )

    @app.exception_handler(BaseTokenException)
    async def base_token_exception_handler(request: Request, exc: BaseTokenException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "token_error", "detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Функция обработчика для всех остальных непойманных исключений.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "internal_server_error", "detail": "Something went wrong"},
        )


# region Token Exceptions
class BaseTokenException(Exception):
    """
    Базовый класс для всех исключений, связанных с токенами.
    """

    pass


class TokenExpiredException(BaseTokenException):
    """
    Исключение для истёкших токенов.
    """

    pass


class InvalidTokenException(BaseTokenException):
    """
    Исключение для недействительных токенов.
    """

    pass
