from flask import current_app
import os
from app.domain.user_information_domain import *
from app.utils.image_upload import upload_image, delete_image
from app.models.user_information import ClientPreferredFieldMapping, PreferredFreelancerMapping

class UserInformationService:
    def __init__(self, user_information_repository, user_id):
        self.user_information_repository = user_information_repository
        self.user_id = user_id
        self.initialize_domain()

    def initialize_domain(self):        

        # 레포지토리에서 데이터를 가져와 도메인 객체 초기화
        user_info_data = self.user_information_repository.get_user_info_by_user_id(self.user_id)

        if user_info_data and user_info_data.get('success'):
            user_info_data = user_info_data['user_info']
            
            # 레포지토리에서 가져온 preferred_fields와 preferred_freelancer 리스트 사용
            preferred_fields = [ClientPreferredFieldMapping(user_id=field['user_id'], field_code=field['field_code'])
                                for field in user_info_data.get('preferred_fields', [])]
            
            preferred_freelancers = [PreferredFreelancerMapping(user_id=freelancer['user_id'], preferred_code=freelancer['preferred_code'])
                                    for freelancer in user_info_data.get('preferred_freelancer', [])]
            
            # 도메인 객체 초기화
            self.user_information_domain = UserInformationDomain(
                user_id=user_info_data['user_id'],
                email=user_info_data['email'],
                nickname=user_info_data['nickname'],
                business_area=user_info_data['business_area'],
                profile_picture_path=user_info_data['profile_picture_path'],
                inquiry_st=user_info_data['inquiry_st'],
                freelancer_registration_st=user_info_data['freelancer_registration_st'],
                created_at=user_info_data['created_at'],
                updated_at=user_info_data['updated_at'],
                preferred_fields=preferred_fields,
                preferred_freelancer=preferred_freelancers
            )
        else:
            raise ValueError("사용자 정보를 찾을 수 없습니다.")

    # 사용자 정보 조회
    def get_user_information(self):
        user_info = self.user_information_domain
        if user_info:
            return {
                'user_id': user_info.user_id,  
                'email': user_info.email,
                'nickname': user_info.nickname,
                'profile_picture_path': user_info.profile_picture_path, 
                'business_area': user_info.business_area,
                'inquiry_st': user_info.inquiry_st,
                'freelancer_registration_st': user_info.freelancer_registration_st,
                'preferred_fields': [
                    {'user_id': field.user_id, 'preferred_code': field.field_code} 
                    for field in user_info.preferred_fields
                ],
                'preferred_freelancer': [
                    {'user_id': preferred_freelancer_item.user_id, 'preferred_code': preferred_freelancer_item.preferred_code} 
                    for preferred_freelancer_item in user_info.preferred_freelancer
                ],
                'created_at': user_info.created_at,  
                'updated_at': user_info.updated_at   
            }
        else:
            return None
    
    # 닉네임 중복 확인
    def check_nickname_availability(self, nickname):
        # 닉네임 유효성 검증
        result = self.user_information_domain.check_nickname(nickname)
        if not result["success"]:
            return result

        # 닉네임 중복 확인
        if self.user_information_repository.check_nickname_duplication(nickname):
            return {"success": False, "message": "중복된 닉네임이 있습니다."}

        return {"success": True, "message": "사용 가능한 닉네임입니다."}

    # 닉네임 변경
    def change_nickname(self, user_id, new_nickname):        
        result = self.user_information_repository.save_new_nickname(user_id, new_nickname)
        if result['success']:
            self.user_information_domain.update_nickname(new_nickname)
            return {"success": True, "message": "새로운 닉네임이 성공적으로 등록되었습니다."}
        else:
            return {"success": False, "message": "닉네임 등록에 실패하였습니다."}
        
    # 비즈니스 영역 변경
    def change_business_area(self, user_id, new_business_area):
        result = self.user_information_repository.save_new_business_area(user_id, new_business_area)
        if result['success']:
            self.user_information_domain.update_business_area(new_business_area)
            return {"success": True, "message": "비즈니스 정보가 성공적으로 업데이트되었습니다."}
        else:
            return {"success": False, "message": "비즈니스 정보 업데이트에 실패하였습니다."}

    # 선호 분야 변경
    def change_preferred_field(self, preferred_codes: list) -> dict:
        for preferred_code in preferred_codes:
            preferred_field_mapping = ClientPreferredFieldMapping(
                user_id=self.user_information_domain.user_id,
                preferred_code=preferred_code
            )
            result = self.user_information_repository.save_preferred_field(preferred_field_mapping)
            
            if result['success']:
                self.user_information_domain.update_preferred_fields(preferred_field_mapping)
            else:
                return {'success': False, 'message': f'{preferred_code} 선호 분야 저장에 실패했습니다.'}
        
        return {'success': True, 'message': '선호 분야가 성공적으로 저장되었습니다.'}

    # 선호 분야 삭제
    def delete_preferred_field(self, preferred_codes: list) -> dict:
        for preferred_code in preferred_codes:
            preferred_field_mapping = ClientPreferredFieldMapping(
                user_id=self.user_information_domain.user_id,
                preferred_code=preferred_code
            )

            # 선호 분야 삭제 로직 호출
            result = self.user_information_repository.delete_preferred_field(preferred_field_mapping)
            
            if not result['success']:
                return {'success': False, 'message': f'{preferred_code} 선호 분야 삭제에 실패했습니다.'}
            
            # 도메인 객체 업데이트
            self.user_information_domain.remove_preferred_fields(preferred_field_mapping)

        return {'success': True, 'message': '선호 분야가 성공적으로 삭제되었습니다.'}

    # 선호하는 프리랜서 변경
    def change_preferred_freelancer(self, preferred_freelancer_codes: list) -> dict:
        for preferred_code in preferred_freelancer_codes:
            preferred_freelancer_mapping = PreferredFreelancerMapping(
                user_id=self.user_information_domain.user_id,
                preferred_code=preferred_code
            )
            result = self.user_information_repository.save_preferred_freelancer(preferred_freelancer_mapping)
            
            if result['success']:
                self.user_information_domain.update_preferred_freelancers(preferred_freelancer_mapping)
            else:
                return {'success': False, 'message': f'{preferred_code} 선호하는 프리랜서 저장에 실패했습니다.'}
        
        return {'success': True, 'message': '선호하는 프리랜서가 성공적으로 저장되었습니다.'}

    # 선호하는 프리랜서 삭제
    def delete_preferred_freelancer(self, preferred_freelancer_codes: list) -> dict:
        for preferred_code in preferred_freelancer_codes:
            preferred_freelancer_mapping = PreferredFreelancerMapping(
                user_id=self.user_information_domain.user_id,
                preferred_code=preferred_code
            )

            # 선호하는 프리랜서 삭제 로직 호출
            result = self.user_information_repository.delete_preferred_freelancer(preferred_freelancer_mapping)
            
            if not result['success']:
                return {'success': False, 'message': f'{preferred_code} 선호하는 프리랜서 삭제에 실패했습니다.'}
            
            # 도메인 객체 업데이트
            self.user_information_domain.remove_preferred_freelancers(preferred_freelancer_mapping)

        return {'success': True, 'message': '선호하는 프리랜서가 성공적으로 삭제되었습니다.'}

    # 프로필 사진 변경
    def change_profile_picture(self, user_id, file):
        # 유틸 함수의 create_user_folder와 일관된 경로 계산
        upload_folder = current_app.config.get('UPLOAD_FOLDER')

        # 도메인 객체에서 현재 프로필 사진 경로 가져오기
        current_profile_picture = self.user_information_domain.profile_picture_path

        # filename이 None일 경우 파일 경로 삭제 로직
        if file is None:
            # 기존 프로필 사진이 있을 경우 삭제
            if current_profile_picture:
                success, error = delete_image(user_id, current_profile_picture)
                if not success:
                    return {"success": False, "message": error}

            # 프로필 사진 경로를 None으로 업데이트
            result = self.user_information_repository.save_profile_picture_path(user_id, None)
            if result['success']:
                self.user_information_domain.update_profile_picture_path(None)
                return {"success": True, "message": "프로필 사진이 성공적으로 삭제되었습니다."}
            return {"success": False, "message": "프로필 사진 경로 삭제에 실패하였습니다."}

        # 파일 업로드 처리 (filename이 None이 아닐 때)
        filename, error = upload_image(file, user_id)
        if error:
            return {"success": False, "message": error}

        # 새 프로필 사진 경로 생성
        new_filepath = os.path.join(upload_folder, str(user_id), filename)

        # 기존 프로필 사진이 있는 경우 삭제
        if current_profile_picture:
            success, error = delete_image(user_id, current_profile_picture)
            if not success:
                return {"success": False, "message": error}

        # 새로운 프로필 사진 경로를 DB에 저장
        result = self.user_information_repository.save_profile_picture_path(user_id, new_filepath)
        if result['success']:
            self.user_information_domain.update_profile_picture_path(new_filepath)
            return {"success": True, "message": "프로필 사진이 성공적으로 업데이트되었습니다."}

        return {"success": False, "message": "프로필 사진 경로 업데이트에 실패하였습니다."}

    # 새로운 회원 등록
    def user_registration(self, user_id: str, email: str, profile_picture_path: Optional[str], 
                        nickname: str, business_area: Optional[str], field_codes: list, 
                        preferred_codes: list) -> dict:
        
        preferred_fields = [ClientPreferredFieldMapping(user_id=user_id, preferred_code=code) for code in field_codes]
        preferred_freelancers = [PreferredFreelancerMapping(user_id=user_id, preferred_code=code) for code in preferred_codes]
        
        # 레포지토리에서 새로운 회원 정보 저장
        result = self.user_information_repository.insert_new_user(
            user_id=user_id,
            email=email,
            profile_picture_path=profile_picture_path,
            nickname=nickname,
            business_area=business_area,
            preferred_fields=preferred_fields,
            preferred_freelancers=preferred_freelancers
        )
        
        # 저장 성공 시 도메인 객체 초기화
        if result['success']:
            self.initialize_domain()
            return {'success': True}
        else:
            return {'success': False, 'message': '사용자 등록에 실패했습니다.'}

    # 프리랜서 등록 상태 확인
    def confirm_freelancer_registration(self) -> bool:
        return self.user_information_domain.freelancer_registration_st

    # 프리랜서 등록 상태 업데이트
    def change_freelancer_registration_state(self, is_registered: bool) -> dict:
        result = self.user_information_repository.update_freelancer_registration_state(self.user_id, is_registered)
        
        if result['success']:
            self.user_information_domain.freelancer_registration_st = is_registered
            return {'success': True}
        else:
            return {'success': False}

    # 문의 상태 확인
    def confirm_inquiry_state(self) -> bool:
        return self.user_information_domain.inquiry_st
    
    # 문의 상태 변경
    def change_inquiry_state(self, user_id: str, inquiry_state: bool) -> dict:
        result = self.user_information_repository.update_inquiry_state(user_id, inquiry_state)
        
        if result['success']:
            self.user_information_domain.update_inquiry_status(inquiry_state)
            return {'success': True}
        else:
            return {'success': False}
