from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.utils.exceptions import (
    IncorrectPasswordException,
    InvalidTokenException,
    PermissionDeniedException,
    TokenExpiredException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.utils.logger_settings import logger


def setup_exception_handlers(app: FastAPI):
    """
    Функция настройки глобальных обработчиков исключений для приложения.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Функция обработчика стандартных HTTP-исключений.
        """

        logger.error(
            "HTTPException",
            method=request.method,
            path=request.url.path,
            status_code=exc.status_code,
            detail=exc.detail,
            client_ip=request.client.host if request.client else None,
        )

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

        logger.warning(
            "ValidationError",
            method=request.method,
            path=request.url.path,
            errors=errors,
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"error": "validation_error", "detail": details},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """
        Функция обработчика ошибок SQLAlchemy.
        """
        logger.error(
            "Database error",
            method=request.method,
            path=request.url.path,
            error=str(exc),
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "database_error", "detail": "DB operation failed"},
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsException,
    ):
        logger.error(
            "UserAlreadyExistsException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "user_already_exists", "detail": str(exc)},
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundException,
    ):
        logger.error(
            "UserNotFoundException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "user_not_found", "detail": str(exc)},
        )

    @app.exception_handler(IncorrectPasswordException)
    async def incorrect_password_handler(
        request: Request,
        exc: IncorrectPasswordException,
    ):
        logger.error(
            "IncorrectPasswordException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "incorrect_password", "detail": str(exc)},
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(
        request: Request,
        exc: InvalidTokenException,
    ):
        logger.error(
            "InvalidTokenException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "invalid_token", "detail": str(exc)},
        )

    @app.exception_handler(TokenExpiredException)
    async def token_expired_exception_handler(
        request: Request,
        exc: TokenExpiredException,
    ):
        logger.error(
            "TokenExpiredException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "token_expired", "detail": str(exc)},
        )

    @app.exception_handler(PermissionDeniedException)
    async def permission_denied_exception_handler(
        request: Request,
        exc: PermissionDeniedException,
    ):
        logger.error(
            "PermissionDeniedException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "permission_denied", "detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Функция обработчика для всех остальных непойманных исключений.
        """
        logger.exception(
            "Unexpected error",
            method=request.method,
            path=request.url.path,
            error=str(exc),
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "detail": "Something went wrong",
            },
        )
