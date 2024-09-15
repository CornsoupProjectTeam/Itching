class UserInformationService:
    def __init__(self, user_information_repository, user_information_domain=None):
        self.user_information_repository = user_information_repository
        self.user_information_domain = user_information_domain

    def check_email(self, user_id):
        # UserInformationRepository의 get_email_by_user_id 메서드를 호출하여 email 반환
        email = self.user_information_repository.get_email_by_user_id(user_id)
        
        # 이메일 값이 있는 경우
        if email:
            return {"success": True, "email": email}
        
        # 이메일 값이 없는 경우
        return {"success": False, "message": "이메일 값을 찾을 수 없습니다."}

    class ChangeNickname:
        def __init__(self, outer_instance):
            self.user_information_repository = outer_instance.user_information_repository
            self.user_information_domain = outer_instance.user_information_domain
            self.is_duplicate_checked = False  # 중복 체크 상태 저장

        def validate_nickname(self, new_nickname):
            # 닉네임 규칙 검사
            is_valid = self.user_information_domain.check_nickname(new_nickname)

            if not is_valid:  # 닉네임 규칙에 맞지 않으면 False 반환
                return {"success": False, "message": "닉네임 규칙에 어긋납니다. 소문자+숫자 조합으로 다시 시도해보세요"}

            # 닉네임 규칙 검사가 성공한 경우에만 중복 검사 수행
            if self.user_information_repository.check_nickname_duplication(new_nickname):
                self.is_duplicate_checked = False  # 중복 확인 실패
                return {"success": False, "message": "중복된 닉네임이 있습니다."}

            # 중복 체크 성공
            self.is_duplicate_checked = True  # 중복 확인 성공
            return {"success": True, "message": "등록 가능한 닉네임 입니다."}

        def save_new_nickname(self, user_id, new_nickname):
            # 중복 체크가 성공했는지 확인
            if not self.is_duplicate_checked:
                return {"success": False, "message": "중복 확인을 먼저 해주세요."}

            # 새로운 닉네임 등록
            if self.user_information_repository.save_new_nickname(user_id, new_nickname):
                return {"success": True, "message": "새로운 닉네임이 등록되었습니다."}
            else:
                return {"success": False, "message": "닉네임 등록에 실패하였습니다."}

    class ChangeBusiness:
        def __init__(self, outer_instance):
            self.user_information_repository = outer_instance.user_information_repository
            self.is_data_checked = False  # 데이터 검증 상태 저장

        # 기존 비즈니스 조회해서 맵핑 데이터로 갖고 오는 로직
        def get_business_by_user_id(self, user_id):
            # UserProfile에서 해당 유저의 비즈니스 정보를 조회
            user_profile = self.user_information_repository.get_user_profile_by_user_id(user_id)
            if user_profile and user_profile.business_area:
                self.is_data_checked = True  # 데이터가 정상적으로 조회되면 상태를 True로 설정
                return {"success": True, "business_area": user_profile.business_area}
            else:
                self.is_data_checked = False  # 데이터가 없으면 상태를 False로 설정
                return {"success": False, "message": "비즈니스 정보를 찾을 수 없습니다."}

        # 수정된 데이터 저장하는 로직
        def save_new_business(self, user_id, new_business_area):
            # 데이터 검증이 먼저 이루어졌는지 확인
            if not self.is_data_checked:
                return {"success": False, "message": "비즈니스 정보를 먼저 확인해주세요."}

            # 새로운 비즈니스 데이터를 UserProfile의 business_area 필드에 저장
            if self.user_information_repository.save_new_business_area(user_id, new_business_area):
                return {"success": True, "message": "비즈니스 정보가 성공적으로 업데이트되었습니다."}
            else:
                return {"success": False, "message": "비즈니스 정보 업데이트에 실패하였습니다."}

    class ChangeInterest:
        def __init__(self, outer_instance):
            self.user_information_repository = outer_instance.user_information_repository
            self.is_data_checked = False  # 데이터 검증 상태 저장

        # 기존 관심사 조회해서 맵핑 데이터로 갖고 오는 로직
        def get_interest_by_user_id(self, user_id):
            # UserProfile에서 해당 유저의 관심사 정보를 조회
            user_profile = self.user_information_repository.get_user_profile_by_user_id(user_id)
            if user_profile and user_profile.interest_area_mapping:
                self.is_data_checked = True  # 데이터가 정상적으로 조회되면 상태를 True로 설정
                return {"success": True, "interest_area_mapping": user_profile.interest_area_mapping}
            else:
                self.is_data_checked = False  # 데이터가 없으면 상태를 False로 설정
                return {"success": False, "message": "관심사 정보를 찾을 수 없습니다."}

        # 수정된 관심사 데이터 저장하는 로직
        def save_new_interest(self, user_id, new_interest_data):
            # 데이터 검증이 먼저 이루어졌는지 확인
            if not self.is_data_checked:
                return {"success": False, "message": "관심사 정보를 먼저 확인해주세요."}

            # 새로운 관심사 데이터를 UserProfile의 interest_area_mapping 필드에 저장
            if self.user_information_repository.save_new_interest_area(user_id, new_interest_data):
                return {"success": True, "message": "관심사 정보가 성공적으로 업데이트되었습니다."}
            else:
                return {"success": False, "message": "관심사 정보 업데이트에 실패하였습니다."}
