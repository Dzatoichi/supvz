from fastapi import Depends

from src.dao.employeesDAO import EmployeesDAO
from src.services.employees_service import EmployeesService

# DAO


def get_employees_repo() -> EmployeesDAO:
    return EmployeesDAO()


# Сервисы


def get_employees_service(
    repo: EmployeesDAO = Depends(get_employees_repo),
) -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService(repo=repo)
