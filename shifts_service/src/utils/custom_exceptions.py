class ShiftNotFoundException(Exception):
    def __init__(self, message: str = "Смена не найдена"):
        self.message = message
        super().__init__(self.message)


class ShiftAlreadyExistsException(Exception):
    def __init__(self, message: str = "Смена уже существует"):
        self.message = message
        super().__init__(self.message)


class ShiftValidationException(Exception):
    def __init__(self, message: str = "Ошибка валидации смены"):
        self.message = message
        super().__init__(self.message)
