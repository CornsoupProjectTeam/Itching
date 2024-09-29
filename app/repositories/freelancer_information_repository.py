import os
from flask import current_app
from models.freelancer_information import *
from sqlalchemy.exc import SQLAlchemyError

class FreelancerInformationRepository:

    def get_public_profile_by_user_id(self, user_id):
        try:
            public_profile = PublicProfile.query.filter_by(user_id=user_id).first()
            return {'success': True, 'public_profile_id': public_profile.public_profile_id} if public_profile else {'success': False, 'message': 'Public profile이 없습니다.'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def save_profile_picture_path(self, public_profile_id: str, new_filepath: str) -> dict:
        try:        
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()

            if public_profile:                
                public_profile.profile_image_path = new_filepath
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

    def save_expertise_field(self, expertise_field: FreelancerExpertiseFieldMapping):
        try:
            db.session.add(expertise_field)
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

    def save_education(self, education: FreelancerEducationMapping):
        try:
            db.session.add(education)
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

    def save_portfolio(self, portfolio: FreelancerPortfolioMapping):
        try:
            db.session.add(portfolio)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
