from ..core.security.permissions import get_permissions_for_role
from ..schemas.users_schemas import UserRole, UserRead

print(f"Direct call: {get_permissions_for_role(UserRole.employee)}")

user_data = {
    "id": 1,
    "email": "test@example.com",  # Добавьте обязательное поле email
    "role": UserRole.employee,
    "created_at": "2023-01-01T00:00:00"
}

user = UserRead(**user_data)
# permissions будет автоматически установлен на основе роли
permission_strings = [p.value for p in user.permissions]
print("All permissions:", ", ".join(permission_strings))