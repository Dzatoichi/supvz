from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.utils.custom_exceptions import (
    ShiftAlreadyExistsException,
    ShiftNotFoundException,
    ShiftValidationException,
)
from src.utils.logger_settings import logger


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(ShiftNotFoundException)
    async def shift_not_found_exception_handler(request: Request, exc: ShiftNotFoundException):
        logger.warning(
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
        logger.warning(
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
        logger.warning(
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

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
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
