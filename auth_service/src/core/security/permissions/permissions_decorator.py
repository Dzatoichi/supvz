from functools import wraps
from flask import request, jsonify
from typing import Callable, List

from .permissions import PermissionEnum, has_permission
from src.models.users.users import UsersRoleEnum


def requires_permission(permissions: List[PermissionEnum]):
    """
    Декоратор для проверки permissions.
    Предполагается, что пользователь уже аутентифицирован и в request есть user_data
    """

    def decorator(f: Callable):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Получаем данные пользователя из request (должны быть установлены middleware аутентификации)
            user_data = getattr(request, 'user_data', None)
            if not user_data:
                return jsonify({"error": "Authentication required"}), 401

            # Получаем роль пользователя
            try:
                user_role = UsersRoleEnum(user_data.get('role'))
            except ValueError:
                return jsonify({"error": "Invalid user role"}), 400

            # Проверяем permissions
            has_required_permission = any(
                has_permission(user_role, perm) for perm in permissions
            )

            if not has_required_permission:
                return jsonify({
                    "error": "Insufficient permissions",
                    "required_permissions": [perm.value for perm in permissions],
                    "user_role": user_role.value
                }), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator