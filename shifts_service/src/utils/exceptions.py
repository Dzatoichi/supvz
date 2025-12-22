from fastapi import HTTPException, status


class ScheduledShiftAlreadyExistsException(HTTPException):
    """Запланированная смена уже существует."""

    def __init__(self, detail: str = "Запланированная смена уже существует"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ScheduledShiftNotFoundException(HTTPException):
    """Запланированная смена не найдена."""

    def __init__(self, detail: str = "Смена не найдена"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ScheduledShiftValidationException(HTTPException):
    """Ошибка валидации данных смены."""

    def __init__(self, detail: str = "Невалидные параметры смены"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ScheduledShiftUpdateException(HTTPException):
    """Ошибка при обновлении запланированной смены."""

    def __init__(self, detail: str = "Ошибка при обновлении смены"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ScheduledShiftDeleteException(HTTPException):
    """Ошибка при удалении запланированной смены."""

    def __init__(self, detail: str = "Ошибка при удалении смены"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
