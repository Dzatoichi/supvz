from enum import Enum


class EventStatus(str, Enum):
    """
    Статусы обработки идемпотентного события.
    """

    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class EventType(str, Enum):
    """
    Типы событий (операций), требующих идемпотентности.
    """

    CREATE_EMPLOYEE = "create_employee"
    UPDATE_EMPLOYEE = "update_employee"
