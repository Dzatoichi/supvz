from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.utils.exceptions import (
    AccessDeniedException,
    EmployeeAlreadyExistsException,
    EmployeeNotAllowedException,
    EmployeeNotFoundException,
    InvalidInternalApiKeyException,
    NoEmployeesInPVZException,
    PVZAlreadyExistsException,
    PVZDeleteFailedException,
    PVZGroupAlreadyExistsException,
    PVZGroupFilterException,
    PVZGroupNotFoundException,
    PVZNotFoundException,
)


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        details = []
        for err in exc.errors():
            if err.get("type") == "string_too_short":
                details.append(f"{err.get('loc')[1]} {err.get('msg').lower()}")
            else:
                details.append(err.get("msg"))

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"error": "validation_error", "detail": details},
        )

    @app.exception_handler(PVZAlreadyExistsException)
    async def pvz_already_exists_handler(
        request: Request,
        exc: PVZAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "pvz_already_exists", "detail": str(exc)},
        )

    @app.exception_handler(PVZNotFoundException)
    async def pvz_not_found_handler(request: Request, exc: PVZNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "pvz_not_found", "detail": str(exc)},
        )

    @app.exception_handler(PVZDeleteFailedException)
    async def pvz_delete_failed_handler(
        request: Request,
        exc: PVZDeleteFailedException,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "pvz_delete_failed", "detail": str(exc)},
        )

    @app.exception_handler(EmployeeAlreadyExistsException)
    async def employee_already_exists_handler(
        request: Request,
        exc: EmployeeAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "employee_already_exists", "detail": str(exc)},
        )

    @app.exception_handler(EmployeeNotFoundException)
    async def employee_not_found_handler(
        request: Request,
        exc: EmployeeNotFoundException,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "employee_not_found", "detail": str(exc)},
        )

    @app.exception_handler(EmployeeNotAllowedException)
    async def employee_not_allowed_handler(
        request: Request,
        exc: EmployeeNotAllowedException,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "employee_not_allowed", "detail": str(exc)},
        )

    @app.exception_handler(NoEmployeesInPVZException)
    async def no_employees_in_pvz_handler(
        request: Request,
        exc: NoEmployeesInPVZException,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "no_employees_in_pvz", "detail": str(exc)},
        )

    @app.exception_handler(PVZGroupAlreadyExistsException)
    async def pvz_group_already_exists_handler(
        request: Request,
        exc: PVZGroupAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "pvz_group_already_exists", "detail": str(exc)},
        )

    @app.exception_handler(PVZGroupNotFoundException)
    async def pvz_group_not_found_handler(
        request: Request,
        exc: PVZGroupNotFoundException,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "pvz_group_not_found", "detail": str(exc)},
        )

    @app.exception_handler(PVZGroupFilterException)
    async def pvz_group_filter_handler(
        request: Request,
        exc: PVZGroupFilterException,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "pvz_group_filter", "detail": str(exc)},
        )

    @app.exception_handler(InvalidInternalApiKeyException)
    async def invalid_internal_api_key_handler(
        request: Request,
        exc: InvalidInternalApiKeyException,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "invalid_internal_api_key", "detail": str(exc)},
        )

    @app.exception_handler(AccessDeniedException)
    async def access_denied_handler(
        request: Request,
        exc: AccessDeniedException,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "access_denied", "detail": str(exc)},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "database_error", "detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "detail": "Something went wrong",
            },
        )
