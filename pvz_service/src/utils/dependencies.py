from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzGroupsDAO import PVZGroupsDAO
from src.dao.pvzsDAO import PVZsDAO
from src.database.base import db_helper
from src.services.employees_service import EmployeesService
from src.services.pvz_groups_service import PVZGroupsService
from src.services.pvz_service import PVZService

# DAO


def get_employees_repo() -> EmployeesDAO:
    return EmployeesDAO()


def get_pvz_repo() -> PVZsDAO:
    return PVZsDAO()


def get_pvz_groups_repo() -> PVZGroupsDAO:
    return PVZGroupsDAO()


# Сервисы


def get_employees_service() -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService()


def get_pvz_service() -> "PVZService":
    """Создает сервис для работы с пользователями."""
    return PVZService()


def get_pvz_groups_service() -> PVZGroupsService:
    """Создает сервис для работы с группами"""
    return PVZGroupsService(db_helper=db_helper)
