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
from src.models.positions.positions import PositionPermissions, Positions

# 3. В конце модели, которые зависят от Users
from src.models.tokens.refresh_tokens import RefreshTokens
from src.models.tokens.stateful_tokens import StatefulTokens

# 2. Затем модели, которые зависят от предыдущих
from src.models.users.users import UserPermissions, Users
