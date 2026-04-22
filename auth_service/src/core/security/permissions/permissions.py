from enum import Enum


class PermissionEnum(str, Enum):
    # Dashboard permissions
    VIEW_DASHBOARD = "dashboard:view"
    CONFIGURE_DASHBOARD = "dashboard:configure"

    # Schedule permissions
    VIEW_SCHEDULE = "schedule:view"
    CREATE_SCHEDULE = "schedule:create"
    EDIT_SCHEDULE = "schedule:edit"
    DELETE_SCHEDULE = "schedule:delete"
    OPEN_SHIFT = "schedule:open"
    CLOSE_SHIFT = "schedule:close"
    MANAGE_SHIFT_REQUESTS = "schedule:manage_requests"

    # Salary permissions
    VIEW_SALARY = "salary:view"
    CALCULATE_SALARY = "salary:calculate"
    PROCESS_SALARY_PAYMENTS = "salary:process_payments"
    MANAGE_SALARY_FORMULAS = "salary:manage_formulas"
    VIEW_SALARY_ADVANCE = "salary:view_advance"
    PROCESS_ADVANCE_PAYMENTS = "salary:process_advance"

    # Requests permissions
    VIEW_REQUESTS = "requests:view"
    CREATE_REQUESTS = "requests:create"
    EDIT_REQUESTS = "requests:edit"
    DELETE_REQUESTS = "requests:delete"
    PROCESS_REQUESTS = "requests:process"
    MANAGE_REQUEST_TYPES = "requests:manage_types"

    # Finance permissions
    VIEW_FINANCE = "finance:view"
    CREATE_TRANSACTIONS = "finance:create_transactions"
    EDIT_TRANSACTIONS = "finance:edit_transactions"
    DELETE_TRANSACTIONS = "finance:delete_transactions"
    VIEW_FINANCIAL_REPORTS = "finance:view_reports"
    MANAGE_PAYMENT_METHODS = "finance:manage_payment_methods"

    # Disputes permissions
    VIEW_DISPUTES = "disputes:view"
    CREATE_DISPUTES = "disputes:create"
    PROCESS_DISPUTES = "disputes:process"

    # Employees permissions
    VIEW_EMPLOYEES = "employees:view"
    CREATE_EMPLOYEES = "employees:create"
    EDIT_EMPLOYEES = "employees:edit"
    DELETE_EMPLOYEES = "employees:delete"
    MANAGE_EMPLOYEE_ROLES = "employees:manage_roles"
    VIEW_EMPLOYEE_DETAILS = "employees:view_details"

    # PVZ permissions
    VIEW_PVZS = "pvzs:view"
    CREATE_PVZS = "pvzs:create"
    EDIT_PVZS = "pvzs:edit"
    DELETE_PVZS = "pvzs:delete"
    MANAGE_PVZ_GROUPS = "pvzs:manage_groups"
    VIEW_PVZ_DETAILS = "pvzs:view_details"
    MANAGE_PVZ_RENT = "pvzs:manage_rent"

    # Payment Schedule permissions
    VIEW_PAYMENT_SCHEDULE = "payment_schedule:view"
    MANAGE_PAYMENT_SCHEDULE = "payment_schedule:manage"

    # Settings permissions
    MANAGE_PERSONAL_SETTINGS = "settings:personal"
    MANAGE_SYSTEM_SETTINGS = "settings:system"

    # Notifications permissions
    VIEW_NOTIFICATIONS = "notifications:view"
    MANAGE_NOTIFICATIONS = "notifications:manage"

    # Audit permissions
    VIEW_AUDIT_LOGS = "audit:view"
