from datetime import datetime, timedelta, timezone

import jwt

from src.settings.config import settings


def create_test_auth_token(user_id: int) -> str:
    """
    Генерирует Access Token для тестов.
    """
    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token
