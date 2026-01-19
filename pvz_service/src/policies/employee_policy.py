from src.dao.employeesDAO import EmployeesDAO
from src.utils.exceptions import AccessDeniedException, EmployeeNotFoundException


class EmployeeAccessPolicy:
    def __init__(self, repo: EmployeesDAO):
        self.repo = repo

    async def check_employee_access(
        self,
        employee_user_id: int,
        current_user_id: int,
    ) -> None:
        """Проверяет, является ли пользователь владельцем сотрудника."""
        employee = await self.repo.get_employee(user_id=employee_user_id)
        if not employee:
            raise EmployeeNotFoundException("Сотрудник не найден")

        if employee.owner_id != current_user_id:
            raise AccessDeniedException("Нет доступа к сотруднику")
