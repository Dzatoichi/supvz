from src.dao.ScheduledShiftsDAO import ScheduledShiftsDAO
from src.services.scheduled_shifts_service import ScheduledShiftsService


def get_scheduled_shifts_dao() -> ScheduledShiftsDAO:
    return ScheduledShiftsDAO()


def get_scheduled_shifts_service() -> ScheduledShiftsService:
    return ScheduledShiftsService()
