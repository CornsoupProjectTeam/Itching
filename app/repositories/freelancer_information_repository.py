from app.models.freelancer_information import *
from sqlalchemy.exc import SQLAlchemyError

class FreelancerInformationRepository:

    def get_public_profile_with_mappings(self, user_id):
            try:
                public_profile = PublicProfile.query.filter_by(user_id=user_id).first()
                if not public_profile:
                    return {'success': False, 'message': 'Public profile이 없습니다.'}

                # PublicProfile_registaration과 관련된 맵핑 데이터를 가져옴
                expertise_fields = FreelancerExpertiseFieldMapping.query.filter_by(public_profile_id=public_profile.public_profile_id).all()
                skill_codes = FreelancerSkillMapping.query.filter_by(public_profile_id=public_profile.public_profile_id).all()
                educations = FreelancerEducationMapping.query.filter_by(public_profile_id=public_profile.public_profile_id).all()
                careers = FreelancerCareerMapping.query.filter_by(public_profile_id=public_profile.public_profile_id).all()
                portfolios = FreelancerPortfolioMapping.query.filter_by(public_profile_id=public_profile.public_profile_id).all()

                # 데이터 반환
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