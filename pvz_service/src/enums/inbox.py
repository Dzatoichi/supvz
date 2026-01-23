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

    # =========================
    # Employees
    # =========================
    CREATE_EMPLOYEE = "create_employee"
    UPDATE_EMPLOYEE = "update_employee"
    DELETE_EMPLOYEE = "delete_employee"

    ASSIGN_EMPLOYEE_TO_PVZ = "assign_employee_to_pvz"
    UNASSIGN_EMPLOYEE_FROM_PVZ = "unassign_employee_from_pvz"

    # =========================
    # PVZ Groups
    # =========================
    CREATE_PVZ_GROUP = "create_pvz_group"
    UPDATE_PVZ_GROUP = "update_pvz_group"
    DELETE_PVZ_GROUP = "delete_pvz_group"

    ASSIGN_RESPONSIBLE_TO_PVZ_GROUP = "assign_responsible_to_pvz_group"

    # =========================
    # PVZ
    # =========================
    CREATE_PVZ = "create_pvz"
    UPDATE_PVZ = "update_pvz"
    DELETE_PVZ = "delete_pvz"

    ASSIGN_PVZ_TO_GROUP = "assign_pvz_to_group"
