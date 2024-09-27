import bcrypt

class EncryptionUtils:

    @staticmethod
    def hash_password(password: str) -> str:
        """비밀번호를 해시 처리합니다."""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        """입력한 비밀번호와 해시된 비밀번호를 비교합니다."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
