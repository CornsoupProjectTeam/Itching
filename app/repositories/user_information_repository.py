#user_information_repository

from mongoengine import DoesNotExist
from models.mongodb_user_information import UserProfile


class UserInformationRepository:
    
    def find_by_user_id(self, user_id: str):
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