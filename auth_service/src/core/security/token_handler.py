from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from src.schemas.tokens import TokenTypesEnum
from src.settings.config import settings


class TokenHandler:
    """
    Class to handle jwt tokens.
    """

    def __init__(self, token_type: TokenTypesEnum) -> None:
        """
        Init function.
        """
        self.algorithm, self.key, self.expire_time = settings.get_jwt_params(token_type=token_type).values()

    def sign_jwt(self, user_id: UUID) -> str:
        """
        Function to encode jwt token.
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.expire_time),
        }
        token = jwt.encode(
            payload=payload,
            key=self.key,
            algorithm=self.algorithm,
        )
        return token, payload.get("exp")

    def decode_jwt(self, token: str) -> dict | None:
        """
        Function to decode jwt token.
        """
        try:
            return jwt.decode(
                token,
                key=self.key,
                algorithms=[self.algorithm],
                options={"require": ["exp"]},
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
