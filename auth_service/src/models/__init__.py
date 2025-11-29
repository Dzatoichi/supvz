__all__ = [
    "Users",
    "UserPermissions",
    "RefreshTokens",
    "StatefulTokens",
    "Permissions",
    "Positions",
    "PositionPermissions",
]


# 1. Сначала базовые модели без зависимостей
from src.models.permissions.permissions import Permissions
from src.models.position_permissions.position_permissions import PositionPermissions
from src.models.positions.positions import Positions

# 3. В конце модели, которые зависят от Users
from src.models.tokens.refresh_tokens import RefreshTokens
from src.models.tokens.stateful_tokens import StatefulTokens
from src.models.user_permissions.user_permissions import UserPermissions

# 2. Затем модели, которые зависят от предыдущих
from src.models.users.users import Users
