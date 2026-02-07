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
