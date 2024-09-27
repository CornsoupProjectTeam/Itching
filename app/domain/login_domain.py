#login_domain.py

from dataclasses import dataclass, field
from typing import Optional
"""아이디, 비밀번호 규칙 설정 추가"""

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
        self.password = new_password
        
    
    def deactivate_user(self):
        self.is_active = False


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
