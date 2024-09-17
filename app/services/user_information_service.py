from app.domain.user_information_domain import UserInformationDomain

class UserInformationService:
    def __init__(self, user_information_repository, user_id):
        self.user_information_repository = user_information_repository

        # 레포지토리에서 UserProfile 데이터를 가져와 도메인 객체 초기화
        user_profile_data = self.user_information_repository.get_user_profile_by_user_id(user_id)
        if user_profile_data:
            self.user_information_domain = UserInformationDomain(user_profile_data)
        else:
            raise ValueError("사용자 정보를 찾을 수 없습니다.")

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
                self.user_information_domain.user_profile.update_nickname(new_nickname)
                
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
            business_area = self.user_information_domain.user_profile.business_area
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
                self.user_information_domain.user_profile.update_business_area(new_business_area)
                
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
            interest_area_mapping = self.user_information_domain.user_profile.interest_area_mapping
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
                self.user_information_domain.user_profile.update_interest_area(new_interest_data)
                
                # 상태 초기화
                self.is_data_checked = False
                return {"success": True, "message": "관심사 정보가 성공적으로 업데이트되었습니다."}
            else:
                return {"success": False, "message": "관심사 정보 업데이트에 실패하였습니다."}