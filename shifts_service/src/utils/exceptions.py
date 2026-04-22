class ShiftNotFoundException(Exception):
    """Исключение: смена не найдена."""

    def __init__(self, message: str = "Смена не найдена"):
        self.message = message
        super().__init__(self.message)


class ShiftAlreadyExistsException(Exception):
    """Исключение: смена уже существует."""

    def __init__(self, message: str = "Смена уже существует"):
        self.message = message
        super().__init__(self.message)


class ShiftValidationException(Exception):
    """Исключение валидации смены."""

    def __init__(self, message: str = "Ошибка валидации смены"):
        self.message = message
        super().__init__(self.message)


class ShiftPenaltyNotFoundException(Exception):
    """Исключение: штраф не найден."""

    def __init__(self, message: str = "Штраф не найден"):
        self.message = message
        super().__init__(self.message)


class ShiftPenaltyAlreadyExistsException(Exception):
    """Исключение: штраф уже существует."""

    def __init__(self, message: str = "Штраф уже существует"):
        self.message = message
        super().__init__(self.message)


class ShiftPenaltyValidationException(Exception):
    """Исключение валидации штрафа."""

    def __init__(self, message: str = "Ошибка валидации штрафа"):
        self.message = message
        super().__init__(self.message)
class ScheduledShiftAlreadyExistsException(Exception):
    """Запланированная смена уже существует."""

    pass


class ScheduledShiftNotFoundException(Exception):
    """Запланированная смена не найдена."""

    pass

class ShiftRequestNotFoundException(Exception):
    """Исключение: запрос на смену не найден."""
class ScheduledShiftValidationException(Exception):
    """Ошибка валидации данных смены."""
    pass

    def __init__(self, message: str = "Запрос на смену не найден"):
        self.message = message
        super().__init__(self.message)
class ScheduledShiftUpdateException(Exception):
    """Ошибка при обновлении запланированной смены."""

    pass

class ShiftRequestAlreadyExistsException(Exception):
    """Исключение: запрос на смену уже существует."""
class ScheduledShiftDeleteException( Exception):
    """Ошибка при удалении запланированной смены."""

    def __init__(self, message: str = "Запрос на смену уже существует"):
        self.message = message
        super().__init__(self.message)
    pass

class ScheduledShiftTimeConflictException(Exception):
    """Конфликт по времени с другими сменами."""
    pass

class ShiftRequestValidationException(Exception):
    """Исключение валидации запроса на смену."""
class ScheduledShiftBusinessLogicException(Exception):
    """Нарушение бизнес-логики."""
    pass

    def __init__(self, message: str = "Ошибка валидации запроса на смену"):
        self.message = message
        super().__init__(self.message)
class PVZNotFoundException(Exception):
    """ПВЗ не найден."""
    pass

class UserNotFoundException(Exception):
    """Пользователь не найден."""
    pass

class ShiftRequestAlreadyProcessedException(Exception):
    """Исключение: запрос на смену уже обработан."""

    def __init__(self, message: str = "Запрос на смену уже обработан"):
        self.message = message
        super().__init__(self.message)


class ShiftRequestShiftAlreadyStartedException(Exception):
    """Исключение: смена уже началась."""

    def __init__(self, message: str = "Смена уже началась"):
        self.message = message
        super().__init__(self.message)


class SalaryRuleNotFoundException(Exception):
    """Исключение: правило расчета зарплаты не найдено."""

    def __init__(self, message: str = "Правило расчета зарплаты не найдено"):
        self.message = message
        super().__init__(self.message)


class SalaryRuleValidationException(Exception):
    """Исключение валидации правила расчета зарплаты."""

    def __init__(self, message: str = "Ошибка валидации правила расчета зарплаты"):
        self.message = message
        super().__init__(self.message)
class UserNotAvailableException(Exception):
    """Пользователь недоступен."""
    pass

class CannotUpdateCompletedShiftException(Exception):
    """Нельзя обновлять выполненную смену."""
    pass

class CannotDeleteCompletedShiftException(Exception):
    """Нельзя удалять выполненную смену."""
    pass