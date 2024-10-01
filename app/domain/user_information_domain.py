import re
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from models.user_information import ClientPreferredFieldMapping, PreferredFreelancerMapping

@dataclass
class UserInformationDomain:
    user_id: str
    email: str
    nickname: str
    business_area: Optional[str]
    profile_picture_path: Optional[str]
    inquiry_st: bool
    freelancer_registration_st: bool
    created_at: datetime
    updated_at: datetime
    
    preferred_fields: List[ClientPreferredFieldMapping]
    preferred_freelancer: List[PreferredFreelancerMapping]

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

    def update_nickname(self, new_nickname: str):
        self.nickname = new_nickname

    def update_business_area(self, new_business_area: str):
        self.business_area = new_business_area

    def update_profile_picture_path(self, new_path: str):
        self.profile_picture_path = new_path
    
    def update_inquiry_status(self, new_inquiry_status: bool):
        self.inquiry_st = new_inquiry_status

    def update_freelancer_registration_state(self, is_registered: bool):
        self.freelancer_registration_st = is_registered

    def update_preferred_fields(self, new_field: ClientPreferredFieldMapping):
        if not any(field.preferred_code == new_field.preferred_code for field in self.preferred_fields):
            self.preferred_fields.append(new_field)

    def remove_preferred_fields(self, preferred_field_mapping: ClientPreferredFieldMapping):
        # 주어진 매핑에 해당하는 선호 분야를 도메인 객체에서 삭제
        to_remove = [field for field in self.preferred_fields if field.preferred_code == preferred_field_mapping.preferred_code]

        for field in to_remove:
            if field in self.preferred_fields:
                self.preferred_fields.remove(field)
            else:
                print(f"오류: {field.preferred_code}가 선호 분야에서 찾을 수 없습니다.")

    def update_preferred_freelancers(self, new_freelancer: PreferredFreelancerMapping):
        if not any(freelancer.preferred_code == new_freelancer.preferred_code for freelancer in self.preferred_freelancers):
            self.preferred_freelancers.append(new_freelancer)

    def remove_preferred_freelancers(self, preferred_freelancer_mapping: PreferredFreelancerMapping):
        # 주어진 매핑에 해당하는 선호하는 프리랜서를 도메인 객체에서 삭제
        to_remove = [freelancer for freelancer in self.preferred_freelancers if freelancer.preferred_code == preferred_freelancer_mapping.preferred_code]

        for freelancer in to_remove:
            if freelancer in self.preferred_freelancers:
                self.preferred_freelancers.remove(freelancer)
            else:
                print(f"오류: {freelancer.preferred_code}가 선호하는 프리랜서에서 찾을 수 없습니다.")
