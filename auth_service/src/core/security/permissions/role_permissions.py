from typing import Optional

from .permissions import PermissionEnum

# Определим базовые группы permissions
VIEW_ONLY_PERMISSIONS = [
    PermissionEnum.VIEW_DASHBOARD,
    PermissionEnum.VIEW_SCHEDULE,
    PermissionEnum.VIEW_SALARY,
    PermissionEnum.VIEW_SALARY_ADVANCE,
    PermissionEnum.VIEW_REQUESTS,
    PermissionEnum.VIEW_FINANCE,
    PermissionEnum.VIEW_FINANCIAL_REPORTS,
    PermissionEnum.VIEW_DISPUTES,
    PermissionEnum.VIEW_EMPLOYEES,
    PermissionEnum.VIEW_EMPLOYEE_DETAILS,
    PermissionEnum.VIEW_PVZS,
    PermissionEnum.VIEW_PVZ_DETAILS,
    PermissionEnum.VIEW_PAYMENT_SCHEDULE,
    PermissionEnum.VIEW_NOTIFICATIONS,
    PermissionEnum.VIEW_AUDIT_LOGS,
    PermissionEnum.MANAGE_PERSONAL_SETTINGS,
]

FULL_OWNER_PERMISSIONS = [
    # Все permissions которые были у owner
    PermissionEnum.VIEW_DASHBOARD,
    PermissionEnum.CONFIGURE_DASHBOARD,
    PermissionEnum.VIEW_SCHEDULE,
    PermissionEnum.CREATE_SCHEDULE,
    PermissionEnum.EDIT_SCHEDULE,
    PermissionEnum.DELETE_SCHEDULE,
    PermissionEnum.OPEN_SHIFT,
    PermissionEnum.CLOSE_SHIFT,
    PermissionEnum.MANAGE_SHIFT_REQUESTS,
    PermissionEnum.VIEW_SALARY,
    PermissionEnum.CALCULATE_SALARY,
    PermissionEnum.PROCESS_SALARY_PAYMENTS,
    PermissionEnum.MANAGE_SALARY_FORMULAS,
    PermissionEnum.VIEW_SALARY_ADVANCE,
    PermissionEnum.PROCESS_ADVANCE_PAYMENTS,
    PermissionEnum.VIEW_REQUESTS,
    PermissionEnum.CREATE_REQUESTS,
    PermissionEnum.EDIT_REQUESTS,
    PermissionEnum.DELETE_REQUESTS,
    PermissionEnum.PROCESS_REQUESTS,
    PermissionEnum.MANAGE_REQUEST_TYPES,
    PermissionEnum.VIEW_FINANCE,
    PermissionEnum.CREATE_TRANSACTIONS,
    PermissionEnum.EDIT_TRANSACTIONS,
    PermissionEnum.DELETE_TRANSACTIONS,
    PermissionEnum.VIEW_FINANCIAL_REPORTS,
    PermissionEnum.MANAGE_PAYMENT_METHODS,
    PermissionEnum.VIEW_DISPUTES,
    PermissionEnum.CREATE_DISPUTES,
    PermissionEnum.PROCESS_DISPUTES,
    PermissionEnum.VIEW_EMPLOYEES,
    PermissionEnum.CREATE_EMPLOYEES,
    PermissionEnum.EDIT_EMPLOYEES,
    PermissionEnum.DELETE_EMPLOYEES,
    PermissionEnum.MANAGE_EMPLOYEE_ROLES,
    PermissionEnum.VIEW_EMPLOYEE_DETAILS,
    PermissionEnum.VIEW_PVZS,
    PermissionEnum.CREATE_PVZS,
    PermissionEnum.EDIT_PVZS,
    PermissionEnum.DELETE_PVZS,
    PermissionEnum.MANAGE_PVZ_GROUPS,
    PermissionEnum.VIEW_PVZ_DETAILS,
    PermissionEnum.MANAGE_PVZ_RENT,
    PermissionEnum.VIEW_PAYMENT_SCHEDULE,
    PermissionEnum.MANAGE_PAYMENT_SCHEDULE,
    PermissionEnum.MANAGE_PERSONAL_SETTINGS,
    PermissionEnum.MANAGE_SYSTEM_SETTINGS,
    PermissionEnum.VIEW_NOTIFICATIONS,
    PermissionEnum.MANAGE_NOTIFICATIONS,
    PermissionEnum.VIEW_AUDIT_LOGS,
]

ROLE_PERMISSIONS = {
    "administrator": FULL_OWNER_PERMISSIONS,
    "owner": FULL_OWNER_PERMISSIONS,
    "curator": [
        # Dashboard permissions
        PermissionEnum.VIEW_DASHBOARD,
        # Schedule permissions (только для прикрепленных ПВЗ)
        PermissionEnum.VIEW_SCHEDULE,
        PermissionEnum.CREATE_SCHEDULE,
        PermissionEnum.EDIT_SCHEDULE,
        PermissionEnum.DELETE_SCHEDULE,
        PermissionEnum.OPEN_SHIFT,
        PermissionEnum.CLOSE_SHIFT,
        PermissionEnum.MANAGE_SHIFT_REQUESTS,
        # Salary permissions (просмотр и расчет)
        PermissionEnum.VIEW_SALARY,
        PermissionEnum.CALCULATE_SALARY,
        PermissionEnum.VIEW_SALARY_ADVANCE,
        # Requests permissions (для прикрепленных ПВЗ)
        PermissionEnum.VIEW_REQUESTS,
        PermissionEnum.CREATE_REQUESTS,
        PermissionEnum.EDIT_REQUESTS,
        PermissionEnum.DELETE_REQUESTS,
        PermissionEnum.PROCESS_REQUESTS,
        # Finance permissions (только просмотр для своих ПВЗ)
        PermissionEnum.VIEW_FINANCE,
        PermissionEnum.CREATE_TRANSACTIONS,
        PermissionEnum.VIEW_FINANCIAL_REPORTS,
        # Disputes permissions
        PermissionEnum.VIEW_DISPUTES,
        PermissionEnum.CREATE_DISPUTES,
        # Employees permissions (для прикрепленных ПВЗ)
        PermissionEnum.VIEW_EMPLOYEES,
        PermissionEnum.CREATE_EMPLOYEES,
        PermissionEnum.EDIT_EMPLOYEES,
        PermissionEnum.VIEW_EMPLOYEE_DETAILS,
        # PVZ permissions (для прикрепленных ПВЗ)
        PermissionEnum.VIEW_PVZS,
        PermissionEnum.EDIT_PVZS,
        PermissionEnum.VIEW_PVZ_DETAILS,
        # Payment Schedule permissions
        PermissionEnum.VIEW_PAYMENT_SCHEDULE,
        # Settings permissions
        PermissionEnum.MANAGE_PERSONAL_SETTINGS,
        PermissionEnum.VIEW_NOTIFICATIONS,
        # Audit permissions (только для своих ПВЗ)
        PermissionEnum.VIEW_AUDIT_LOGS,
    ],
    "employee": [
        # Dashboard permissions
        PermissionEnum.VIEW_DASHBOARD,
        # Schedule permissions (только свои смены)
        PermissionEnum.VIEW_SCHEDULE,
        PermissionEnum.OPEN_SHIFT,
        PermissionEnum.CLOSE_SHIFT,
        # Requests permissions (только свои заявки)
        PermissionEnum.VIEW_REQUESTS,
        PermissionEnum.CREATE_REQUESTS,
        # Salary permissions (только свои начисления)
        PermissionEnum.VIEW_SALARY,
        # Settings permissions
        PermissionEnum.MANAGE_PERSONAL_SETTINGS,
        PermissionEnum.VIEW_NOTIFICATIONS,
    ],
    "intern": [
        # Минимальные права для стажера
        PermissionEnum.VIEW_DASHBOARD,
        PermissionEnum.VIEW_SCHEDULE,
        PermissionEnum.OPEN_SHIFT,
        PermissionEnum.CLOSE_SHIFT,
        PermissionEnum.VIEW_REQUESTS,
        PermissionEnum.CREATE_REQUESTS,
        PermissionEnum.VIEW_SALARY,
        PermissionEnum.MANAGE_PERSONAL_SETTINGS,
        PermissionEnum.VIEW_NOTIFICATIONS,
    ],
    "handyman": [
        # Права для разнорабочего (расширенные compared to employee)
        PermissionEnum.VIEW_DASHBOARD,
        PermissionEnum.VIEW_SCHEDULE,
        PermissionEnum.OPEN_SHIFT,
        PermissionEnum.CLOSE_SHIFT,
        PermissionEnum.VIEW_REQUESTS,
        PermissionEnum.CREATE_REQUESTS,
        PermissionEnum.EDIT_REQUESTS,  # Может редактировать свои заявки
        PermissionEnum.VIEW_SALARY,
        PermissionEnum.MANAGE_PERSONAL_SETTINGS,
        PermissionEnum.VIEW_NOTIFICATIONS,
        # Дополнительные права для хозяйственных работ
        PermissionEnum.VIEW_PVZS,  # Может просматривать ПВЗ для выполнения работ
    ],
}


# Содержит все подписки для овнера
SUBSCRIPTION_PERMISSIONS = {
    "paid": FULL_OWNER_PERMISSIONS,
    "test": FULL_OWNER_PERMISSIONS,
    "expired": VIEW_ONLY_PERMISSIONS,
}


def get_permissions_for_role(role: str, subscription: Optional[str] = None) -> list[PermissionEnum]:
    """Получить permissions для роли с учетом подписки."""
    base_permissions = ROLE_PERMISSIONS.get(role, [])

    if role == "owner" and subscription:
        return SUBSCRIPTION_PERMISSIONS.get(subscription, base_permissions)

    return base_permissions


def has_permission(role: str, permission: PermissionEnum, subscription: Optional[str] = None) -> bool:
    """Проверить наличие permission у роли с учетом подписки."""
    user_permissions = get_permissions_for_role(role, subscription)
    return permission in user_permissions
