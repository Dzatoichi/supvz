from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.utils.exceptions import (
    ShiftAlreadyExistsException,
    ShiftNotFoundException,
    ShiftPenaltyAlreadyExistsException,
    ShiftPenaltyNotFoundException,
    ShiftPenaltyValidationException,
    ShiftValidationException,
)
from src.utils.logger_settings import logger


def setup_exception_handlers(app: FastAPI):
    """Настройка обработчиков исключений."""

    @app.exception_handler(ShiftNotFoundException)
    async def shift_not_found_exception_handler(request: Request, exc: ShiftNotFoundException):
        """Обработчик ошибки: смена не найдена."""
        logger.error(
            "ShiftNotFoundException",
            method=request.method,
            path=request.url.path,
            detail=exc.message,
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "not_found", "detail": exc.message},
        )

    @app.exception_handler(ShiftAlreadyExistsException)
    async def shift_already_exists_exception_handler(request: Request, exc: ShiftAlreadyExistsException):
        """Обработчик ошибки: смена уже существует."""
        logger.error(
            "ShiftAlreadyExistsException",
            method=request.method,
            path=request.url.path,
            detail=exc.message,
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "conflict", "detail": exc.message},
        )

    @app.exception_handler(ShiftValidationException)
    async def shift_validation_exception_handler(request: Request, exc: ShiftValidationException):
        """Обработчик ошибки: ошибка валидации смены."""
        logger.error(
            "ShiftValidationException",
            method=request.method,
            path=request.url.path,
            detail=exc.message,
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "validation_error", "detail": exc.message},
        )

    @app.exception_handler(ShiftPenaltyNotFoundException)
    async def shift_penalty_not_found_exception_handler(request: Request, exc: ShiftPenaltyNotFoundException):
        """Обработчик ошибки: штраф не найден."""
        logger.error(
            "ShiftPenaltyNotFoundException",
            method=request.method,
            path=request.url.path,
            detail=exc.message,
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "not_found", "detail": exc.message},
        )

    @app.exception_handler(ShiftPenaltyAlreadyExistsException)
    async def shift_penalty_already_exists_exception_handler(request: Request, exc: ShiftPenaltyAlreadyExistsException):
        """Обработчик ошибки: штраф уже существует."""
        logger.error(
            "ShiftPenaltyAlreadyExistsException",
            method=request.method,
            path=request.url.path,
            detail=exc.message,
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "conflict", "detail": exc.message},
        )

    @app.exception_handler(ShiftPenaltyValidationException)
    async def shift_penalty_validation_exception_handler(request: Request, exc: ShiftPenaltyValidationException):
        """Обработчик ошибки: ошибка валидации штрафа."""
        logger.error(
            "ShiftPenaltyValidationException",
            method=request.method,
            path=request.url.path,
            detail=exc.message,
            client_ip=request.client.host if request.client else None,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "validation_error", "detail": exc.message},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Обработчик стандартных HTTP-исключений."""
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
        """Обработчик ошибок валидации запросов."""
        errors = exc.errors()
        details = []
        for err in errors:
            if err.get("type") == "string_too_short":
                details.append(str(err.get("loc")[1]) + " " + str(err.get("msg")).lower())
            else:
                details.append(str(err.get("msg")))

        logger.error(
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
        """Обработчик ошибок базы данных."""
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

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Обработчик неожиданных ошибок."""
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
