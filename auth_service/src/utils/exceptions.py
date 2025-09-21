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
            content={"error": "http_error", "detail": exc.detail, "path": request.url.path},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Функция обработчика ошибок валидации входящих данных.
        """
        errors = exc.errors()
        for err in errors:
            ctx = err.get("ctx")
            if ctx and "error" in ctx and isinstance(ctx["error"], Exception):
                ctx["error"] = str(ctx["error"])
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "detail": errors,
                "body": exc.body,
                "path": request.url.path,
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """
        Функция обработчика ошибок SQLAlchemy.
        """
        print("Database error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "database_error", "detail": "DB operation failed"},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Функция обработчика для всех остальных непойманных исключений.
        """
        print("Unexpected error: %s", exc)
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