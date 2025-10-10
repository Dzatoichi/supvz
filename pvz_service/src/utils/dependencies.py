from fastapi import Depends
from pvz_service.src.dao.pvzsDAO import PVZsDAO
from pvz_service.src.services.pvz_service import PVZService

from src.dao.employeesDAO import EmployeesDAO
from src.services.employees_service import EmployeesService


def get_employees_repo() -> EmployeesDAO:
    return EmployeesDAO()


def get_employees_service(
    repo: EmployeesDAO = Depends(get_employees_repo),
) -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService()


def get_pvzs_service() -> PVZService:
    return PVZService()


def get_pvzs_dao() -> PVZsDAO:
    return PVZsDAO()
