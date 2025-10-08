from src.services.employees_service import EmployeesService
from src.dao.pvzsDAO import PVZsDAO
from src.services.pvz_service import PVZService


def get_employees_service() -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService()


def get_pvzs_service() -> PVZService:
    return PVZService()


def get_pvzs_dao() -> PVZsDAO:
    return PVZsDAO()
