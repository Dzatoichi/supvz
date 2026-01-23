class PVZAlreadyExistsException(Exception):
    pass


class PVZNotFoundException(Exception):
    pass


class PVZDeleteFailedException(Exception):
    pass


class EmployeeAlreadyExistsException(Exception):
    pass


class EmployeeNotFoundException(Exception):
    pass


class EmployeeNotAllowedException(Exception):
    pass


class NoEmployeesInPVZException(Exception):
    pass


class PVZGroupAlreadyExistsException(Exception):
    pass


class PVZGroupNotFoundException(Exception):
    pass


class PVZGroupFilterException(Exception):
    pass


class InvalidInternalApiKeyException(Exception):
    pass


class AccessDeniedException(Exception):
    pass


class InboxConflictException(Exception):
    """
    Вызывается, когда запрос уже обрабатывается другим процессом (Processing).
    Ожидаемое поведение: вернуть 409 Conflict.
    """

    pass
    # def __init__(self, message: str = "Запрос уже обрабатывается", retry_after: int = 10):
    #     self.message = message
    #     self.retry_after = retry_after
    #     super().__init__(message)
