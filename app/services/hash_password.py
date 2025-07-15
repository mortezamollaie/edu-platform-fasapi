from passlib.context import CryptContext

class Hash:
    """
    Utility class for password hashing using bcrypt.
    """

    def __init__(self) -> None:
        """
        Initialize the password hashing context with bcrypt algorithm.
        """
        self.pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def bcrypt(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)
