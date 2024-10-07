from app.models.freelancer_information import *
from datetime import datetime
import pytz
from sqlalchemy.exc import SQLAlchemyError

class FreelancerRegistrationRepository:

    # user_id로 public_profile 존재 여부를 확인하는 메서드
    def has_public_profile(self, user_id):
        try:
            public_profile = PublicProfile.query.filter_by(user_id=user_id).first()
            
            # 프로필이 존재하면 success와 함께 public_profile_id 반환, 없으면 False 반환
            if public_profile:
                return {'success': True, 'public_profile_id': public_profile.public_profile_id}
            else:
                return {'success': False, 'message': '공개 프로필이 없습니다.'}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    # public_profile_id로 공개 프로필과 세부 정보 가져오는 메서드
    def get_public_profile_for_registration(self, public_profile_id):
        try:          
            # public_profile을 가져옴
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            
            if not public_profile:                
                return {'success': False, 'message': '공개 프로필을 찾을 수 없습니다.'}

            # 각 맵핑 테이블에서 public_profile_id를 기준으로 데이터 가져옴
            expertise_fields = FreelancerExpertiseFieldMapping.query.filter_by(public_profile_id=public_profile_id).all()

            skill_codes = FreelancerSkillMapping.query.filter_by(public_profile_id=public_profile_id).all()
        
            educations = FreelancerEducationMapping.query.filter_by(public_profile_id=public_profile_id).all()

            careers = FreelancerCareerMapping.query.filter_by(public_profile_id=public_profile_id).all()
        
            portfolios = FreelancerPortfolioMapping.query.filter_by(public_profile_id=public_profile_id).all()
            

            # 공개 프로필과 함께 세부 데이터 반환
            return {
                'success': True,
                'profile': public_profile,
                'expertise_fields': expertise_fields,
                'skill_codes': skill_codes,
                'educations': educations,
                'careers': careers,
                'portfolios': portfolios
            }
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def create_new_public_profile(self, profile_data: dict) -> dict:
        try:
            # 새로운 공개 프로필 생성
            new_profile = PublicProfile(
                public_profile_id=profile_data['public_profile_id'],
                user_id=profile_data['user_id'],
                nickname=profile_data['nickname']
            )
            db.session.add(new_profile)
            db.session.commit()
            return {'success': True, 'message': '공개 프로필이 성공적으로 생성되었습니다.'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_profile_picture_path(self, public_profile_id: str, new_filepath: str) -> dict:
        try:        
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()

            if public_profile:
                # PublicProfile의 profile_image_path 업데이트                
                public_profile.profile_image_path = new_filepath

                # PublicProfileList의 profile_image_path 업데이트
                public_profile_list = PublicProfileList.query.filter_by(public_profile_id=public_profile_id).first()
                if public_profile_list:
                    public_profile_list.profile_image_path = new_filepath
                
                db.session.commit()
                return {'success': True}
            
            return {'success': False, 'message': 'Public profile이 없습니다.'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def get_profile_picture_path(self, public_profile_id: str) -> dict:
        try:            
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            
            if public_profile:
                return {'success': True, 'profile_picture_path': public_profile.profile_image_path}
            return {'success': False, 'message': 'Public profile이 없습니다.'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_freelancer_intro(self, public_profile_id, intro_text):
        try:
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if public_profile:
                public_profile.freelancer_intro = intro_text
                db.session.commit()
                return {'success': True}
            return {'success': False, 'message': 'Public profile이 없습니다.'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_sns_link(self, public_profile_id, sns_link):
        try:
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if public_profile:
                public_profile.sns_link = sns_link
                db.session.commit()
                return {'success': True}
            return {'success': False, 'message': 'Public profile이 없습니다.'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_expertise_field(self, expertise_field: FreelancerExpertiseFieldMapping):
        try:
            db.session.add(expertise_field)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def delete_expertise_field(self, expertise_field: FreelancerExpertiseFieldMapping):
        try:
            FreelancerExpertiseFieldMapping.query.filter_by(
                public_profile_id=expertise_field.public_profile_id,
                field_code=expertise_field.field_code
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_skill_code(self, skill_code: FreelancerSkillMapping):
        try:
            db.session.add(skill_code)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def delete_skill_code(self, skill_mapping: FreelancerSkillMapping):
        try:
            FreelancerSkillMapping.query.filter_by(
                public_profile_id=skill_mapping.public_profile_id,
                skill_code=skill_mapping.skill_code
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_education(self, education: FreelancerEducationMapping):
        try:
            db.session.add(education)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def delete_education(self, education: FreelancerEducationMapping):
        try:
            FreelancerEducationMapping.query.filter_by(
                public_profile_id=education.public_profile_id,
                school=education.school
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_career(self, career: FreelancerCareerMapping):
        try:
            db.session.add(career)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def delete_career(self, career_mapping: FreelancerCareerMapping):
        try:
            FreelancerCareerMapping.query.filter_by(
                public_profile_id=career_mapping.public_profile_id,
                company=career_mapping.company,
                role=career_mapping.role
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_portfolio(self, portfolio: FreelancerPortfolioMapping):
        try:
            db.session.add(portfolio)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def delete_portfolio(self, portfolio_mapping: FreelancerPortfolioMapping):
        try:
            FreelancerPortfolioMapping.query.filter_by(
                public_profile_id=portfolio_mapping.public_profile_id,
                image_path=portfolio_mapping.image_path
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def save_registration_date(self, public_profile_id):
        try:
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if public_profile:
                # 현재 UTC 시간 가져오기
                utc_now = datetime.utcnow()
                
                # UTC 시간을 한국 시간으로 변환
                korean_tz = pytz.timezone('Asia/Seoul')
                korean_time = utc_now.replace(tzinfo=pytz.utc).astimezone(korean_tz)
                
                # 한국 시간으로 freelancer_registration_date 저장
                public_profile.freelancer_registration_date = korean_time
                formatted_time = korean_time.strftime('%Y-%m-%d %H:%M:%S')
                
                # 세션 커밋
                db.session.commit()
                return {'success': True, 'registration_date': formatted_time}
            return {'success': False, 'message': 'Public profile이 없습니다.'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    # PublicProfileList 생성
    def create_public_profile_list(self, public_profile_id, nickname, profile_image_path, freelancer_registration_date, freelancer_badge):
        try:
            # 새로운 PublicProfileList 객체 생성
            public_profile_list = PublicProfileList(
                public_profile_id=public_profile_id,
                nickname=nickname,
                profile_image_path=profile_image_path,
                freelancer_registration_date=freelancer_registration_date,
                freelancer_badge=freelancer_badge
            )
            
            db.session.add(public_profile_list)
            db.session.commit()
            
            return {"success": True, "message": "PublicProfileList가 성공적으로 생성되었습니다."}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"success": False, "message": f"PublicProfileList 생성에 실패했습니다: {str(e)}"}