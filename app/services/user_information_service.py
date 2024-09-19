from app.domain.user_information_domain import UserInformationDomain
from app.utils.image_upload import upload_image, delete_image

class UserInformationService:
    def __init__(self, user_information_repository, user_id):
        self.user_information_repository = user_information_repository

        # 레포지토리에서 MongoEngine 모델 데이터를 가져옴
        user_info_data = self.user_information_repository.get_user_info_by_user_id(user_id)
        
        # MongoEngine 모델 데이터를 도메인 객체로 변환
        if user_info_data:
            self.user_information_domain = UserInformationDomain(
                user_id=user_info_data.user_id,
                email=user_info_data.email,
                nickname=user_info_data.nickname,
                business_area=user_info_data.business_area,
                interest_area_mapping=user_info_data.interest_area_mapping,
                profile_picture_path=user_info_data.profile_picture_path,
                created_at=user_info_data.created_at,
                updated_at=user_info_data.updated_at
            )
        else:
            raise ValueError("사용자 정보를 찾을 수 없습니다.")
    
        # 중첩 클래스를 인스턴스화하고 속성으로 노출
        self.change_nickname = self.ChangeNickname(self.user_information_domain, self.user_information_repository)
        self.change_business = self.ChangeBusiness(self.user_information_domain, self.user_information_repository)
        self.change_interest = self.ChangeInterest(self.user_information_domain, self.user_information_repository)
        self.change_profile_picture = self.ChangeProfilePicture(self.user_information_domain, self.user_information_repository)

    # user_id로 사용자 정보를 조회
    def get_user_information(self):
        user_info = self.user_information_domain
        if user_info:
            return {
                'user_id': user_info.user_id,  
                'email': user_info.email,
                'nickname': user_info.nickname,
                'profile_picture_path': user_info.profile_picture_path, 
                'business_area': user_info.business_area,
                'interest_area_mapping': user_info.interest_area_mapping,
                'created_at': user_info.created_at,  
                'updated_at': user_info.updated_at   
            }
        else:
            return None


    class ChangeNickname:
        def __init__(self, user_information_domain, user_information_repository):
            self.user_information_domain = user_information_domain  # 이미 초기화된 도메인 객체 재사용
            self.user_information_repository = user_information_repository
            self.is_duplicate_checked = False  # 중복 체크 상태 저장

        def validate_nickname(self, new_nickname):
            # 도메인 계층에서 닉네임 규칙 검증
            result = self.user_information_domain.check_nickname(new_nickname)

            if not result["success"]:
                return result

            # 닉네임 규칙 검사가 성공한 경우에만 중복 검사 수행
            if self.user_information_repository.check_nickname_duplication(new_nickname):
                self.is_duplicate_checked = False
                return {"success": False, "message": "중복된 닉네임이 있습니다."}

            # 중복 체크 성공
            self.is_duplicate_checked = True
            return {"success": True, "message": "등록 가능한 닉네임입니다."}

        def save_new_nickname(self, user_id, new_nickname):
            if not self.is_duplicate_checked:
                return {"success": False, "message": "중복 확인을 먼저 해주세요."}

            # 서비스 계층에서 닉네임 업데이트 처리
            if self.user_information_repository.save_new_nickname(user_id, new_nickname):
                # 도메인 객체의 닉네임 업데이트
                self.user_information_domain.update_nickname(new_nickname)  
                
                # 상태 초기화
                self.is_duplicate_checked = False
                return {"success": True, "message": "새로운 닉네임이 성공적으로 등록되었습니다."}
            else:
                return {"success": False, "message": "닉네임 등록에 실패하였습니다."}

    class ChangeBusiness:
        def __init__(self, user_information_domain, user_information_repository):
            self.user_information_domain = user_information_domain 
            self.user_information_repository = user_information_repository
            self.is_data_checked = False

        def get_business_by_user_id(self):
            # 도메인 객체에서 business_area를 가져옴
            business_area = self.user_information_domain.business_area  
            if business_area:
                self.is_data_checked = True
                return {"success": True, "business_area": business_area}
            else:
                self.is_data_checked = False
                return {"success": False, "message": "비즈니스 정보를 찾을 수 없습니다."}

        def save_new_business(self, user_id, new_business_area):
            if not self.is_data_checked:
                return {"success": False, "message": "비즈니스 정보를 먼저 확인해주세요."}

            # 서비스 계층에서 비즈니스 영역 업데이트 처리
            if self.user_information_repository.save_new_business_area(user_id, new_business_area):
                # 도메인 객체의 business_area 업데이트
                self.user_information_domain.update_business_area(new_business_area)  
                
                # 상태 초기화
                self.is_data_checked = False
                return {"success": True, "message": "비즈니스 정보가 성공적으로 업데이트되었습니다."}
            else:
                return {"success": False, "message": "비즈니스 정보 업데이트에 실패하였습니다."}

    class ChangeInterest:
        def __init__(self, user_information_domain, user_information_repository):
            self.user_information_domain = user_information_domain 
            self.user_information_repository = user_information_repository
            self.is_data_checked = False

        def get_interest_by_user_id(self, user_id):
            # 도메인 객체에서 interest_area_mapping을 가져옴
            interest_area_mapping = self.user_information_domain.interest_area_mapping  
            if interest_area_mapping:
                self.is_data_checked = True
                return {"success": True, "interest_area_mapping": interest_area_mapping}
            else:
                self.is_data_checked = False
                return {"success": False, "message": "관심사 정보를 찾을 수 없습니다."}

        def save_new_interest(self, user_id, new_interest_data):
            if not self.is_data_checked:
                return {"success": False, "message": "관심사 정보를 먼저 확인해주세요."}

            # 서비스 계층에서 관심사 데이터 업데이트 처리
            if self.user_information_repository.save_new_interest_area(user_id, new_interest_data):
                # 도메인 객체의 interest_area_mapping 업데이트
                self.user_information_domain.update_interest_area(new_interest_data)  
                
                # 상태 초기화
                self.is_data_checked = False
                return {"success": True, "message": "관심사 정보가 성공적으로 업데이트되었습니다."}
            else:
                return {"success": False, "message": "관심사 정보 업데이트에 실패하였습니다."}
            
    class ChangeProfilePicture:
        def __init__(self, user_information_domain, user_information_repository):
            self.user_information_domain = user_information_domain
            self.user_information_repository = user_information_repository

        def upload_profile_picture(self, user_id, file):
            filename, error = upload_image(file, user_id)
            
            if error:
                return {"success": False, "message": error}
            
            if self.user_information_repository.save_profile_picture_path(user_id, filename):
                # 도메인 객체의 profile_picture_path 업데이트
                self.user_information_domain.update_profile_picture_path(filename)  
                return {"success": True, "message": "프로필 사진이 성공적으로 업로드되었습니다."}
            else:
                return {"success": False, "message": "프로필 사진 경로 업데이트에 실패하였습니다."}

        def delete_profile_picture(self, user_id):
            current_picture_path = self.user_information_repository.get_profile_picture_path(user_id)
            
            if not current_picture_path:
                return {"success": False, "message": "삭제할 프로필 사진이 없습니다."}

            success, error = delete_image(user_id, current_picture_path)
            
            if not success:
                return {"success": False, "message": error}

            if self.user_information_repository.save_profile_picture_path(user_id, None):
                # 도메인 객체의 profile_picture_path 업데이트
                self.user_information_domain.update_profile_picture_path(None)  
                return {"success": True, "message": "프로필 사진이 성공적으로 삭제되었습니다."}
            else:
                return {"success": False, "message": "프로필 사진 경로 삭제에 실패하였습니다."}