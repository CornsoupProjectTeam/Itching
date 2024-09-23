#identity_verification_domain.py

from datetime import datetime
import re

class IdentityVerificationDomain:
    def __init__(self, phone_number, verification_code, expiration_time):
        self.phone_number = phone_number
        self.verification_code = verification_code
        self.expiration_time = expiration_time

    def is_valid_phone_number(self):
        # 전화번호 유효성 검사 (10~15 자리 숫자)
        pattern = r"^\d{10,15}$"
        return re.match(pattern, self.phone_number) is not None

    def is_verification_code_valid(self, input_code):
        # 인증 코드가 일치하고 만료되지 않았는지 확인
        if self.verification_code == input_code and datetime.utcnow() <= self.expiration_time:
            return True
        return False
