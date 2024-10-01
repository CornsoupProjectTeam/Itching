#user_information_repository
from flask import current_app
import os
from mongoengine import DoesNotExist
from app.models.user_information import UserInformation


class UserInformationRepository:

    def get_user_info_by_user_id(self, user_id: str) -> dict:
        try:
            # 기본 사용자 정보 조회
            user_info = UserInformation.query.filter_by(user_id=user_id).first()

            if not user_info:
                return {'success': False, 'message': '사용자를 찾을 수 없습니다.'}

            # preferred_fields 리스트 가져오기
            preferred_fields = ClientPreferredFieldMapping.query.filter_by(user_id=user_id).all()
            preferred_fields_list = [{'user_id': field.user_id, 'preferred_code': field.preferred_code} for field in preferred_fields]

            # preferred_freelancer 리스트 가져오기
            preferred_freelancers = PreferredFreelancerMapping.query.filter_by(user_id=user_id).all()
            preferred_freelancers_list = [{'user_id': freelancer.user_id, 'preferred_code': freelancer.preferred_code} for freelancer in preferred_freelancers]

            # 사용자 정보와 함께 반환
            return {
                'success': True,
                'user_info': {
                    'user_id': user_info.user_id,
                    'email': user_info.email,
                    'nickname': user_info.nickname,
                    'business_area': user_info.business_area,
                    'profile_picture_path': user_info.profile_picture_path,
                    'inquiry_st': user_info.inquiry_st,
                    'freelancer_registration_st': user_info.freelancer_registration_st,
                    'created_at': user_info.created_at,
                    'updated_at': user_info.updated_at,
                    'preferred_fields': preferred_fields_list,
                    'preferred_freelancer': preferred_freelancers_list
                }
            }
        except Exception as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)}
        
    def check_user_id_duplication(self, user_id: str) -> bool:
        # 주어진 user_id가 중복되는지 확인
        try:
            return UserInformation.query.filter_by(user_id=user_id).count() > 0
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)}  

    def check_nickname_duplication(self, nickname: str) -> bool:
        # 주어진 닉네임이 중복되는지 확인
        try:
            return UserInformation.query.filter_by(nickname=nickname).count() > 0
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 
    
    def save_new_nickname(self, user_id: str, new_nickname: str) -> dict:
        # 주어진 user_id의 닉네임을 새로운 닉네임으로 업데이트
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                user_info.nickname = new_nickname
                db.session.commit()
                return {'success': True}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 

    def save_freelancer_registration(self, user_id: str, status: bool) -> dict:
        # 주어진 user_id의 프리랜서 등록 상태를 업데이트
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                user_info.freelancer_registration_st = status
                db.session.commit()
                return {'success': True}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 

    def update_inquiry_status(self, user_id: str, status: bool) -> dict:
        # 주어진 user_id의 문의 상태를 업데이트
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                user_info.inquiry_st = status
                db.session.commit()
                return {'success': True}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 
        
    def insert_new_user(self, user_id: str, email: str, profile_picture_path: Optional[str], 
                    nickname: str, business_area: Optional[str], 
                    preferred_fields: list, preferred_freelancers: list) -> dict:
        try:
            # 새로운 사용자 정보 저장
            new_user = UserInformation(
                user_id=user_id,
                email=email,
                profile_picture_path=profile_picture_path,
                nickname=nickname,
                business_area=business_area
            )
            db.session.add(new_user)
            
            # preferred_fields 저장
            for field in preferred_fields:
                new_preferred_field = ClientPreferredFieldMapping(
                    user_id=field.user_id, 
                    preferred_code=field.preferred_code
                )
                db.session.add(new_preferred_field)

            # preferred_freelancers 저장
            for freelancer in preferred_freelancers:
                new_preferred_freelancer = PreferredFreelancerMapping(
                    user_id=freelancer.user_id, 
                    preferred_code=freelancer.preferred_code
                )
                db.session.add(new_preferred_freelancer)

            db.session.commit()
            return {'success': True}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def get_user_by_email(self, email: str) -> dict:
        # 주어진 이메일로 사용자 정보를 조회
        try:
            user_info = UserInformation.query.filter_by(email=email).first()
            if user_info:
                return {'success': True, 'user_info': user_info}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 

    def get_email_by_user_id(self, user_id: str) -> dict:
        # 주어진 user_id로 이메일을 조회
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                return {'success': True, 'email': user_info.email}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 

    def save_new_business_area(self, user_id: str, new_business_area: str) -> dict:
        # 주어진 user_id의 business_area를 새로운 비즈니스 영역으로 업데이트
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                user_info.business_area = new_business_area
                db.session.commit()
                return {'success': True}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 

    def save_profile_picture_path(self, user_id: str, new_filepath: str) -> dict:
        try:
            user_info = self.get_user_info_by_user_id(user_id)['user_info']

            if user_info:
                user_info.profile_picture_path = new_filepath
                db.session.commit()
                return {'success': True}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 

    def get_profile_picture_path(self, user_id: str) -> dict:
        try:            
            user_info = self.get_user_info_by_user_id(user_id)['user_info']
            if user_info:
                return {'success': True, 'profile_picture_path': user_info.profile_picture_path}
            return {'success': False, 'message': '프로필 사진 경로를 찾을 수 없습니다.'}

        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 

    # 선호 분야 저장
    def save_preferred_field(self, preferred_field_mapping: ClientPreferredFieldMapping) -> dict:
        try:
            db.session.add(preferred_field_mapping)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    # 선호 분야 삭제
    def delete_preferred_field(self, preferred_field_mapping: ClientPreferredFieldMapping) -> dict:
        try:
            # 해당하는 user_id와 preferred_code를 기준으로 삭제
            ClientPreferredFieldMapping.query.filter_by(
                user_id=preferred_field_mapping.user_id,
                preferred_code=preferred_field_mapping.preferred_code
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    # 선호하는 프리랜서 저장
    def save_preferred_freelancer(self, preferred_freelancer_mapping: PreferredFreelancerMapping) -> dict:
        try:
            db.session.add(preferred_freelancer_mapping)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    # 선호하는 프리랜서 삭제
    def delete_preferred_freelancer(self, preferred_freelancer_mapping: PreferredFreelancerMapping) -> dict:
        try:
            # 해당하는 user_id와 preferred_code를 기준으로 삭제
            PreferredFreelancerMapping.query.filter_by(
                user_id=preferred_freelancer_mapping.user_id,
                preferred_code=preferred_freelancer_mapping.preferred_code
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
        
    def check_freelancer_registration(self, user_id: str) -> bool:
        # 주어진 user_id의 프리랜서 등록 상태를 확인
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                return user_info.freelancer_registration_st
            return False  # 유저가 없으면 False 반환
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 
    
    def update_freelancer_registration_state(self, user_id: str, is_registered: bool) -> dict:
        try:
            # 주어진 user_id의 정보를 조회
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:                
                user_info.freelancer_registration_st = is_registered
                db.session.commit()
                return {'success': True}
            return {'success': False}
        except SQLAlchemyError as e:
            db.session.rollback()  
            return {'success': False, 'message': str(e)} 