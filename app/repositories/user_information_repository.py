#user_information_repository
from mongoengine import DoesNotExist
from models.mongodb_user_information import UserProfile


class UserInformationRepository:
    
    def get_user_profile_by_user_id(self, user_id: str):
        # 주어진 user_id로 사용자 정보를 조회
        try:
            return UserProfile.objects.get(user_id=user_id)
        except DoesNotExist:
            return None

    def check_user_id_duplication(self, user_id: str) -> bool:
        # 주어진 user_id가 중복되는지 확인
        return UserProfile.objects(user_id=user_id).count() > 0

    def check_nickname_duplication(self, nickname: str) -> bool:
        # 주어진 닉네임이 중복되는지 확인
        return UserProfile.objects(nickname=nickname).count() > 0

    def update_freelancer_registration(self, user_id: str, status: bool) -> bool:
        # 주어진 user_id의 프리랜서 등록 상태를 업데이트
        user_profile = self.find_by_user_id(user_id)
        if user_profile:
            user_profile.update(freelancer_registration_status=status)
            return True
        return False

    def update_inquiry_status(self, user_id: str, status: bool) -> bool:
        # 주어진 user_id의 문의 상태를 업데이트
        user_profile = self.find_by_user_id(user_id)
        if user_profile:
            user_profile.update(inquiry_status=status)
            return True
        return False

    def insert_user(self, user_info: dict):
        # 새 사용자 정보를 삽입
        if not self.check_user_id_duplication(user_info['user_id']):
            user_profile = UserProfile(**user_info)
            user_profile.save()
            return True
        return False

    def get_user_by_email(self, email: str):
        # 주어진 이메일로 사용자 정보를 조회
        try:
            return UserProfile.objects.get(email=email)
        except DoesNotExist:
            return None
        
    def save_new_nickname(self, user_id: str, new_nickname: str) -> bool:
        # 주어진 user_id의 닉네임을 새로운 닉네임으로 업데이트
        user_profile = self.get_user_profile_by_user_id(user_id)
        if user_profile:
            user_profile.update(nickname=new_nickname)
            return True
        return False

    def get_email_by_user_id(self, user_id: str):
        # 주어진 user_id로 이메일을 조회
        user_profile = self.get_user_profile_by_user_id(user_id)
        if user_profile:
            return user_profile.email
        return None

    def save_new_business_area(self, user_id: str, new_business_area: str) -> bool:
        # 주어진 user_id의 business_area를 새로운 비즈니스 영역으로 업데이트
        user_profile = self.get_user_profile_by_user_id(user_id)
        if user_profile:
            user_profile.update(business_area=new_business_area)
            return True
        return False

    def save_new_interest_area(self, user_id: str, new_interest_data: dict) -> bool:
        # 주어진 user_id의 interest_area_mapping을 새로운 관심사 데이터로 업데이트
        user_profile = self.get_user_profile_by_user_id(user_id)
        if user_profile:
            user_profile.update(interest_area_mapping=new_interest_data)
            return True
        return False