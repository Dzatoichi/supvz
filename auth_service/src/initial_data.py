import asyncio

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database.base import db_helper
from src.models import Permissions, SystemPositions
from src.models.position_permissions.position_permissions import SystemPositionPermissions

# --- КОНФИГУРАЦИЯ ДАННЫХ ---

# 1. Список прав доступа (Permissions)
# Формат: code_name: description
DEFINED_PERMISSIONS = {
    "system:admin": "Полный доступ к системе (Superuser)",
    "analytics:view_global": "Просмотр статистики по всей сети",
    "analytics:view_pvz": "Просмотр статистики конкретного ПВЗ",
    "pvz:create": "Создание новых пунктов выдачи",
    "pvz:edit": "Редактирование информации о ПВЗ",
    "pvz:delete": "Удаление пунктов выдачи",
    "users:manage_all": "Управление всеми пользователями",
    "users:manage_staff": "Управление сотрудниками (найм/увольнение)",
    "orders:process": "Обработка заказов (приемка/выдача)",
    "finance:view": "Просмотр финансовых отчетов",
}

# 2. Список должностей (SystemPositions) и их прав
# Формат: Title: [list of permission code_names]
DEFINED_POSITIONS = {
    "Администратор": [
        "system:admin",
        "analytics:view_global",
        "analytics:view_pvz",
        "pvz:create",
        "pvz:edit",
        "pvz:delete",
        "users:manage_all",
        "users:manage_staff",
        "orders:process",
        "finance:view",
    ],
    "Владелец сети": [
        "analytics:view_global",
        "analytics:view_pvz",
        "pvz:create",
        "pvz:edit",
        "users:manage_staff",
        "finance:view",
    ],
    "Куратор": ["analytics:view_pvz", "pvz:edit", "users:manage_staff", "finance:view"],
    "Менеджер ПВЗ": ["analytics:view_pvz", "users:manage_staff", "orders:process"],
    "Сотрудник ПВЗ": ["orders:process"],
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
