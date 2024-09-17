import re
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class UserProfile:
    user_id: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    business_area: Optional[str] = None
    interest_area_mapping: Optional[dict] = None

    def update_nickname(self, new_nickname):
        self.nickname = new_nickname

    def update_business_area(self, new_business_area):
        self.business_area = new_business_area

    def update_interest_area(self, new_interest_data):
        self.interest_area_mapping = new_interest_data


class UserInformationDomain:
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile

    def check_nickname(self, new_nickname: str):
        # 닉네임이 영어 소문자와 숫자로만 이루어졌는지 확인하는 정규 표현식
        pattern = r'^[a-z0-9]+$'

        # 닉네임 길이가 20자를 초과하면 False 반환
        if len(new_nickname) > 20:
            return {"success": False, "message": "닉네임은 20자를 초과할 수 없습니다."}

        # 정규 표현식에 맞는지 확인
        if not re.match(pattern, new_nickname):
            return {"success": False, "message": "닉네임은 영어 소문자와 숫자로만 이루어져야 합니다."}

        # 닉네임 규칙이 통과된 경우
        return {"success": True, "message": "닉네임이 유효합니다."}
