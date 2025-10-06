import hashlib

from passlib.context import CryptContext


class HashHelper:
    """
    Класс для обработки паролей и хеширования токенов.
    """

    def __init__(self):
        """
        Метод инициализации.
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, plain_str: str) -> str:
        """
        Метод хеширования строк (для паролей).
        """
        return self.pwd_context.hash(plain_str)

    def hash_token(self, token: str) -> str:
        """
        Метод хеширования токенов (deterministic).
        """
        return hashlib.sha256(token.encode()).hexdigest()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Метод верификации пароля.
        """
        return self.pwd_context.verify(plain_password, hashed_password)


hash_helper = HashHelper()
