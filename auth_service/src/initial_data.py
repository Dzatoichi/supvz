import asyncio

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database.base import db_helper
from src.models import Permissions, SystemPositions
from src.models.position_permissions.system_position_permissions import SystemPositionPermissions

# --- КОНФИГУРАЦИЯ ДАННЫХ ---

# 1. Список прав доступа (Permissions)
# Формат: code_name: description
DEFINED_PERMISSIONS = {
    "auth:generate_register_token": "Генерация токена для регистрации сотрудника",
    "permissions:get": "Получение списка всех доступных прав",
    # Позиции (должности)
    "positions:get": "Получение списка позиций",
    "position:get": "Получение информации о конкретной позиции",
    "position:create": "Создание новой позиции",
    "position:update": "Редактирование существующей позиции",
    "position:delete": "Удаление позиции",
    # Управление пользователями и правами
    "user:update_permissions": "Изменение прав доступа конкретного пользователя",
    "users:update_permissions": "Массовое управление правами пользователей",
    # Сотрудники
    "employee:get": "Просмотр профиля сотрудника",
    "employees:get": "Просмотр списка всех сотрудников (для руководства)",
    "employee:assign_to_pvz": "Привязка сотрудника к определенному ПВЗ",
    "employee:unassign_from_pvz": "Отвязка сотрудника от ПВЗ",
    "employee:delete": "Удаление профиля сотрудника и связанного аккаунта",
    # Группы ПВЗ
    "pvz_groups:get": "Просмотр списка групп ПВЗ",
    "pvz_groups:create": "Создание новой группы ПВЗ",
    "pvz_group:get": "Получение информации о группе ПВЗ",
    "pvz_group:update": "Редактирование параметров группы ПВЗ",
    "pvz_group:delete": "Удаление группы ПВЗ",
    "pvz_group:assign_responsible": "Назначение ответственного лица за группу ПВЗ",
    # Пункты выдачи заказов (ПВЗ)
    "pvz:get": "Просмотр информации о ПВЗ",
    "pvzs:get": "Просмотр списка всех ПВЗ",
    "pvz:create": "Регистрация нового ПВЗ в системе",
    "pvz:update": "Обновление данных ПВЗ",
    "pvz:delete": "Удаление ПВЗ из системы",
    "pvz:assign_to_group": "Добавление ПВЗ в группу",
    "pvzs:get_employees": "Просмотр списка коллег на ПВЗ (для рядовых сотрудников)",
    # Смены
    "shift:get": "Просмотр информации о смене",
    "shifts:get": "Просмотр расписания смен",
    "shift:create": "Создание/планирование новой смены",
    "shift:update": "Редактирование параметров смены",
    "shift:delete": "Отмена или удаление смены",
    # Заявки (Requests)
    "requests:get": "Получение списка всех заявок",
    "request:get": "Просмотр деталей конкретной заявки",
    "request:create": "Создание новой заявки",
    "request:update": "Частичное обновление данных заявки (например, смена статуса)",
    "request:delete": "Удаление заявки",
    # Назначения по заявкам (Assignments)
    "request_assignments:get": "Просмотр списка назначений по заявкам",
    "request_assignment:get": "Просмотр деталей назначения",
    "request_assignment:create": "Назначение исполнителя на заявку",
    "request_assignment:update": "Изменение параметров назначения",
}

# 2. Список должностей (SystemPositions) и их прав
# Формат: Title: [list of permission code_names]
DEFINED_POSITIONS = {
    "owner": list(DEFINED_PERMISSIONS.keys()),
    "curator": [
        "auth:generate_register_token",
        "positions:get",
        "position:get",
        "employee:get",
        "employees:get",
        "employee:assign_to_pvz",
        "employee:unassign_from_pvz",
        "employee:delete",
        "pvz_groups:get",
        "pvz_group:get",
        "pvz:get",
        "pvzs:get",
        "pvzs:get_employees",
        "shift:get",
        "shifts:get",
        "shift:create",
        "shift:update",
        "shift:delete",
        "requests:get",
        "request:get",
        "request:create",
        "request:update",
        "request:delete",
        "request_assignments:get",
        "request_assignment:get",
        "request_assignment:create",
    ],
    "pvz_manager": [
        "employee:get",
        "pvz:get",
        "pvzs:get",
        "pvzs:get_employees",
        "shift:get",
        "shifts:get",
        "requests:get",
        "request:get",
        "request:create",
        "request:update",
        "request:delete",
        "request_assignments:get",
        "request_assignment:get",
    ],
    "handyman": [
        "pvzs:get_employees",
        "requests:get",
        "request:get",
        "request:create",
        "request:updates",
        "request_assignments:get",
        "request_assignment:get",
        "request_assignment:create",
        "request_assignment:update",
    ],
}


async def init_db_data():
    async with db_helper.async_session_maker() as session:
        # 1. Создаем или обновляем Permissions
        permission_objects = {}  # Словарь для хранения объектов {code_name: PermissionObj}

        for code, desc in DEFINED_PERMISSIONS.items():
            stmt = select(Permissions).where(Permissions.code_name == code)
            result = await session.execute(stmt)
            perm = result.scalar_one_or_none()

            if not perm:
                perm = Permissions(code_name=code, description=desc)
                session.add(perm)
            else:
                # Обновляем описание, если оно изменилось
                if perm.description != desc:
                    perm.description = desc

            # Сохраняем объект в словарь для дальнейшего использования
            # Флашим, чтобы получить ID, если объект новый
            permission_objects[code] = perm

        await session.flush()

        # 2. Создаем или обновляем SystemPositions
        position_objects = {}  # Словарь {title: PositionObj}

        for title in DEFINED_POSITIONS.keys():
            stmt = select(SystemPositions).where(SystemPositions.title == title)
            result = await session.execute(stmt)
            pos = result.scalar_one_or_none()

            if not pos:
                pos = SystemPositions(title=title)
                session.add(pos)

            position_objects[title] = pos

        await session.flush()

        # 3. Настраиваем связи (SystemPositionPermissions)
        for pos_title, perm_codes in DEFINED_POSITIONS.items():
            position = position_objects[pos_title]

            for code in perm_codes:
                permission = permission_objects.get(code)
                if not permission:
                    continue

                # Проверяем, существует ли уже такая связь
                link_stmt = select(SystemPositionPermissions).where(
                    SystemPositionPermissions.system_position_id == position.id,
                    SystemPositionPermissions.permission_id == permission.id,
                )
                link_res = await session.execute(link_stmt)
                existing_link = link_res.scalar_one_or_none()

                if not existing_link:
                    new_link = SystemPositionPermissions(system_position_id=position.id, permission_id=permission.id)
                    session.add(new_link)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
        except Exception:
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(init_db_data())
