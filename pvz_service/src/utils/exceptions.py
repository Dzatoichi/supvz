from abc import ABC


class AppException(Exception, ABC):
    """
    Базовый класс для всех бизнес-исключений.

    Содержит метаданные для:
    - InboxService (определение 4xx/5xx)
    - Exception handlers (формирование response)
    """

    status_code: int = 500
    error_code: str = "internal_error"

    def __init__(self, detail: str = ""):
        self.detail = detail
        super().__init__(detail)

    def to_response(self) -> dict:
        """Сериализация для сохранения в response_body."""
        return {
            "status_code": self.status_code,
            "error": self.error_code,
            "detail": self.detail,
        }

    @property
    def is_client_error(self) -> bool:
        """4xx ошибка - идемпотентная, не ретраить."""
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """5xx ошибка - можно ретраить."""
        return self.status_code >= 500


# ─────────────── 400 Bad Request ───────────────


class ClientException(AppException):
    """Базовый класс для 4xx ошибок."""

    status_code = 400


class PVZGroupFilterException(ClientException):
    status_code = 400
    error_code = "pvz_group_filter"


# ─────────────── 403 Forbidden ───────────────


class AccessDeniedException(ClientException):
    status_code = 403
    error_code = "access_denied"


class EmployeeNotAllowedException(ClientException):
    status_code = 403
    error_code = "employee_not_allowed"


class InvalidInternalApiKeyException(ClientException):
    status_code = 403
    error_code = "invalid_internal_api_key"


# ─────────────── 404 Not Found ───────────────


class PVZNotFoundException(ClientException):
    status_code = 404
    error_code = "pvz_not_found"


class EmployeeNotFoundException(ClientException):
    status_code = 404
    error_code = "employee_not_found"


class NoEmployeesInPVZException(ClientException):
    status_code = 404
    error_code = "no_employees_in_pvz"


class PVZGroupNotFoundException(ClientException):
    status_code = 404
    error_code = "pvz_group_not_found"


# ─────────────── 409 Conflict ───────────────


class PVZAlreadyExistsException(ClientException):
    status_code = 409
    error_code = "pvz_already_exists"


class EmployeeAlreadyExistsException(ClientException):
    status_code = 409
    error_code = "employee_already_exists"


class PVZGroupAlreadyExistsException(ClientException):
    status_code = 409
    error_code = "pvz_group_already_exists"


class InboxConflictException(ClientException):
    """
    Вызывается, когда запрос уже обрабатывается другим процессом.
    Ожидаемое поведение: вернуть 409 Conflict.
    """

    status_code = 409
    error_code = "inbox_conflict"


class EventRaceConditionError(ClientException):
    """
    Исключение, возникающее при конкурентном доступе к InboxEvents.
    """

    status_code = 409
    error_code = "event_race_condition"


# ─────────────── 500 Conflict ───────────────


class ServerException(AppException):
    """Базовый класс для 5xx ошибок."""

    status_code = 500


class PVZDeleteFailedException(ServerException):
    status_code = 500
    error_code = "pvz_delete_failed"


class DatabaseException(ServerException):
    status_code = 503
    error_code = "database_error"
