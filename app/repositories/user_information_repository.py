from app.utils.image_upload import delete_image
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
import os
from models.freelancer_information import UserInformation, db

class UserInformationRepository:

    def get_user_info_by_user_id(self, user_id):
        # 주어진 user_id로 사용자 정보를 조회
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                return {'success': True, 'user_info': user_info}
            return {'success': False}
        except SQLAlchemyError as e:
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
        
    def insert_user(self, user_info: dict) -> dict:
        # 새 사용자 정보를 삽입
        if not self.check_user_id_duplication(user_info['user_id']):
            try:
                new_user = UserInformation(**user_info)
                db.session.add(new_user)
                db.session.commit()
                return {'success': True}
            except SQLAlchemyError as e:
                db.session.rollback()  
                return {'success': False, 'message': str(e)} 
        return {'success': False}

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

    def save_new_interest_area(self, user_id: str, new_interest_data: dict) -> dict:
        # 주어진 user_id의 interest_area_mapping을 새로운 관심사 데이터로 업데이트
        try:
            user_info = UserInformation.query.filter_by(user_id=user_id).first()
            if user_info:
                user_info.interest_area_mapping = new_interest_data
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