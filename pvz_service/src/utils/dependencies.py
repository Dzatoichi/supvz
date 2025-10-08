from src.services.employees_service import EmployeesService


def get_employees_service() -> "EmployeesService":
    """Создает сервис для работы с пользователями."""
    return EmployeesService()
