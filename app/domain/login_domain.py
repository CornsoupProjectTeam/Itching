#login_domain.py

from dataclasses import dataclass, field
from typing import Optional
import re

@dataclass
class User:
    user_id: str
    provider_id: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None  # 이메일 속성 추가
    is_active: bool = True
    created_at: str = ""
    updated_at: str = ""
        
    def change_password(self, new_password: str):
        if self.validate_password(new_password):
            self.password = new_password
        else:
            raise ValueError("Password must be at least 8 characters long and contain only lowercase letters and numbers.")

    def deactivate_user(self):
        self.is_active = False

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        """아이디는 소문자 영어와 숫자만 포함 가능"""
        return bool(re.match(r"^[a-z0-9]+$", user_id))

    @staticmethod
    def validate_password(password: str) -> bool:
        """비밀번호는 소문자 영어와 숫자만 포함 가능"""
        return len(password) >= 8 and bool(re.match(r"^[a-z0-9]+$", password))


@dataclass
class Credentials:
    user_id: str
    password: str

@dataclass
class AuthToken:
    token: str
    expires_at: str

@dataclass
class LoginSession:
    user_id: str
    session_id: str
    token: AuthToken
    created_at: str
    updated_at: str
