from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.utils.exceptions import (
    ScheduledShiftAlreadyExistsException,
    ScheduledShiftNotFoundException,
    ScheduledShiftValidationException,
    ScheduledShiftTimeConflictException,
    ScheduledShiftBusinessLogicException,
    UserNotFoundException,
    UserNotAvailableException,
    CannotUpdateCompletedShiftException,
    CannotDeleteCompletedShiftException,
    PVZNotFoundException,
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

    @app.exception_handler(ScheduledShiftAlreadyExistsException)
    async def scheduled_shift_already_exists_handler(
            request: Request,
            exc: ScheduledShiftAlreadyExistsException,
    ):
        logger.error(
            "ScheduledShiftAlreadyExistsException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "sheduled_shift_already_exists", "detail": str(exc)},
        )

    @app.exception_handler(ScheduledShiftValidationException)
    async def scheduled_shift_validation_handler(
            request: Request,
            exc: ScheduledShiftValidationException,
    ):
        logger.error(
            "ScheduledShiftValidationException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "scheduled_shift_validation_error", "detail": str(exc)},
        )

    @app.exception_handler(ScheduledShiftNotFoundException)
    async def scheduled_shift_not_found_handler(
            request: Request,
            exc: ScheduledShiftNotFoundException,
    ):
        logger.error(
            "ScheduledShiftNotFoundException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "scheduled_shift_not_found", "detail": str(exc)},
        )

    @app.exception_handler(ScheduledShiftTimeConflictException)
    async def scheduled_shift_time_conflict_handler(
            request: Request,
            exc: ScheduledShiftTimeConflictException,
    ):
        logger.error(
            "ScheduledShiftTimeConflictException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "scheduled_shift_time_conflict", "detail": str(exc)},
        )

    @app.exception_handler(ScheduledShiftBusinessLogicException)
    async def scheduled_shift_business_logic_handler(
            request: Request,
            exc: ScheduledShiftBusinessLogicException,
    ):
        logger.error(
            "ScheduledShiftBusinessLogicException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "scheduled_shift_business_logic_error", "detail": str(exc)},
        )

    @app.exception_handler(PVZNotFoundException)
    async def pvz_not_found_handler(
            request: Request,
            exc: PVZNotFoundException,
    ):
        logger.error(
            "PVZNotFoundException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "pvz_not_found", "detail": str(exc)},
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

    @app.exception_handler(UserNotAvailableException)
    async def user_not_available_handler(
            request: Request,
            exc: UserNotAvailableException,
    ):
        logger.error(
            "UserNotAvailableException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "user_not_available", "detail": str(exc)},
        )

    @app.exception_handler(CannotUpdateCompletedShiftException)
    async def cannot_update_completed_shift_handler(
            request: Request,
            exc: CannotUpdateCompletedShiftException,
    ):
        logger.error(
            "CannotUpdateCompletedShiftException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "cannot_update_completed_shift", "detail": str(exc)},
        )

    @app.exception_handler(CannotDeleteCompletedShiftException)
    async def cannot_delete_completed_shift_handler(
            request: Request,
            exc: CannotDeleteCompletedShiftException,
    ):
        logger.error(
            "CannotDeleteCompletedShiftException",
            method=request.method,
            path=request.url.path,
            detail=str(exc),
            client_ip=request.client.host if request.client else None,
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "cannot_delete_completed_shift", "detail": str(exc)},
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
