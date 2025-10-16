from fastapi import Depends

from src.dao.employeesDAO import EmployeesDAO
from src.dao.pvzsDAO import PVZsDAO
from src.services.employees_service import EmployeesService

# DAO


def get_employees_repo() -> EmployeesDAO:
    return EmployeesDAO()


def get_pvz_repo() -> PVZsDAO:
    return PVZsDAO()


# Сервисы


def get_employees_service() -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService()
