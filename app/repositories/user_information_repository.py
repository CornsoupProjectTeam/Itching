#user_information_repository
from flask import current_app
import os
from mongoengine import DoesNotExist
from app.models.user_information import UserInformation


class UserInformationRepository:
    
    def get_user_info_by_user_id(self, user_id: str):
        # 주어진 user_id로 사용자 정보를 조회
        try:
            return UserInformation.objects.get(user_id=user_id)
        except DoesNotExist:
            return None

    def check_user_id_duplication(self, user_id: str) -> bool:
        # 주어진 user_id가 중복되는지 확인
        return UserInformation.objects(user_id=user_id).count() > 0

    def check_nickname_duplication(self, nickname: str) -> bool:
        # 주어진 닉네임이 중복되는지 확인
        return UserInformation.objects(nickname=nickname).count() > 0

    def save_freelancer_registration(self, user_id: str, status: str) -> bool:
        # 주어진 user_id의 프리랜서 등록 상태를 업데이트
        user_info = self.find_by_user_id(user_id)
        if user_info:
            user_info.update(freelancer_registration_status=status)
            return True
        return False

    def update_inquiry_status(self, user_id: str, status: bool) -> bool:
        # 주어진 user_id의 문의 상태를 업데이트
        user_info = self.find_by_user_id(user_id)
        if user_info:
            user_info.update(inquiry_status=status)
            return True
        return False

    def insert_user(self, user_info: dict):
        # 새 사용자 정보를 삽입
        if not self.check_user_id_duplication(user_info['user_id']):
            user_info = UserInformation(**user_info)
            user_info.save()
            return True
        return False

    def get_user_by_email(self, email: str):
        # 주어진 이메일로 사용자 정보를 조회
        try:
            return UserInformation.objects.get(email=email)
        except DoesNotExist:
            return None
        
    def save_new_nickname(self, user_id: str, new_nickname: str) -> bool:
        # 주어진 user_id의 닉네임을 새로운 닉네임으로 업데이트
        user_info = self.get_user_profile_by_user_id(user_id)
        if user_info:
            user_info.update(nickname=new_nickname)
            return True
        return False

    def get_email_by_user_id(self, user_id: str):
        # 주어진 user_id로 이메일을 조회
        user_info = self.get_user_profile_by_user_id(user_id)
        if user_info:
            return user_info.email
        return None

    def save_new_business_area(self, user_id: str, new_business_area: str) -> bool:
        # 주어진 user_id의 business_area를 새로운 비즈니스 영역으로 업데이트
        user_info = self.get_user_profile_by_user_id(user_id)
        if user_info:
            user_info.update(business_area=new_business_area)
            return True
        return False

    def save_new_interest_area(self, user_id: str, new_interest_data: dict) -> bool:
        # 주어진 user_id의 interest_area_mapping을 새로운 관심사 데이터로 업데이트
        user_info = self.get_user_profile_by_user_id(user_id)
        if user_info:
            user_info.update(interest_area_mapping=new_interest_data)
            return True
        return False
    
    def save_profile_picture_path(self, user_id: str, filename: str) -> bool:
        # 유틸 함수의 create_user_folder와 일관된 경로 계산
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        
        # filename이 None일 경우 경로를 생성하지 않음
        if filename is None:
            # 파일 경로를 삭제 (프로필 사진 경로를 None으로 업데이트)
            user_info = self.get_user_info_by_user_id(user_id)
            if user_info:
                user_info.update(profile_picture_path=None)
                return True
            return False
        
        # filename이 None이 아닐 경우에만 경로를 생성
        filepath = os.path.join(upload_folder, str(user_id), filename)
        
        # 프로필 사진 경로를 업데이트
        user_info = self.get_user_info_by_user_id(user_id)
        if user_info:
            user_info.update(profile_picture_path=filepath)
            return True
        return False

    def get_profile_picture_path(self, user_id: str):
        # 사용자의 현재 프로필 사진 경로를 가져오는 메서드
        user_info = self.get_user_info_by_user_id(user_id)
        return user_info.profile_picture_path if user_info else None
