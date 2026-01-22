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
