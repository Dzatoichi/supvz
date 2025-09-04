from passlib.context import CryptContext


class HashHelper:
    """
    Class to handle password hashing.
    """

    def __init__(self):
        """
        Init function.
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, plain_str: str) -> str:
        """
        Function to hash string.
        """
        return self.pwd_context.hash(plain_str)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Function to verify password.
        """
        return self.pwd_context.verify(plain_password, hashed_password)


hash_helper = HashHelper()
