class ScheduledShiftAlreadyExistsException(Exception):
    """Запланированная смена уже существует."""

    pass


class ScheduledShiftNotFoundException(Exception):
    """Запланированная смена не найдена."""

    pass

class ScheduledShiftValidationException(Exception):
    """Ошибка валидации данных смены."""
    pass

class ScheduledShiftUpdateException(Exception):
    """Ошибка при обновлении запланированной смены."""

    pass

class ScheduledShiftDeleteException( Exception):
    """Ошибка при удалении запланированной смены."""

    pass

class ScheduledShiftTimeConflictException(Exception):
    """Конфликт по времени с другими сменами."""
    pass

class ScheduledShiftBusinessLogicException(Exception):
    """Нарушение бизнес-логики."""
    pass

class PVZNotFoundException(Exception):
    """ПВЗ не найден."""
    pass

class UserNotFoundException(Exception):
    """Пользователь не найден."""
    pass

class UserNotAvailableException(Exception):
    """Пользователь недоступен."""
    pass

class CannotUpdateCompletedShiftException(Exception):
    """Нельзя обновлять выполненную смену."""
    pass

class CannotDeleteCompletedShiftException(Exception):
    """Нельзя удалять выполненную смену."""
    pass