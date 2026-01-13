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
    """Исключение: штраф смены не найден."""

    def __init__(self, message: str = "Штраф смены не найден"):
        self.message = message
        super().__init__(self.message)


class ShiftPenaltyAlreadyExistsException(Exception):
    """Исключение: штраф смены уже существует."""

    def __init__(self, message: str = "Штраф смены уже существует"):
        self.message = message
        super().__init__(self.message)


class ShiftPenaltyValidationException(Exception):
    """Исключение валидации штрафа смены."""

    def __init__(self, message: str = "Ошибка валидации штрафа смены"):
        self.message = message
        super().__init__(self.message)
