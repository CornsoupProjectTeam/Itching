from flask import current_app
import os
from app.domain.freelancer_information_domain import *
from app.services.user_information_service import update_freelancer_registration_state
from app.utils.image_upload import upload_image, delete_image
from app.utils.id_generator import generate_public_profile_id
from models.freelancer_information import (
    FreelancerExpertiseFieldMapping,
    FreelancerSkillMapping,
    FreelancerEducationMapping,
    FreelancerCareerMapping,
    FreelancerPortfolioMapping
)

class FreelancerInformation:
    def __init__(self, public_profile_repository, user_id):
        self.repository = public_profile_repository
        self.user_id = user_id

        # 중첩 클래스를 인스턴스화하고 속성으로 노출
        self.freelancer_registration = self.FreelancerRegistration(self.repository, self.user_id)

    class FreelancerRegistration:
        def __init__(self, public_profile_repository, user_id):
            self.repository = public_profile_repository
            self.user_id = user_id
            self.domain = self.initialize_domain()

        def initialize_domain(self):
            # PublicProfileRepository에서 public_profile과 관련된 맵핑 데이터를 가져옴
            profile_data = self.repository.get_public_profile_with_mappings(self.user_id)
            
            if not profile_data['success']:
                # 프로필이 없을 경우 새 프로필을 생성
                new_profile_id = generate_public_profile_id()
                empty_profile = FreelancerRegistration(
                    public_profile_id=new_profile_id,
                    user_id=self.user_id,
                    profile_image_path=None,
                    freelancer_intro=None,
                    expertise_fields=[],
                    skill_codes=[],
                    educations=[],
                    careers=[],
                    sns_link=None,
                    portfolios=[],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                return FreelancerInformationDomain(empty_profile)

            # 프로필과 맵핑 데이터가 있는 경우 도메인 객체 초기화
            public_profile = profile_data['profile']
            expertise_fields = profile_data['expertise_fields']
            skill_codes = profile_data['skill_codes']
            educations = profile_data['educations']
            careers = profile_data['careers']
            portfolios = profile_data['portfolios']

            # 도메인 객체에 데이터를 설정
            complete_profile = FreelancerRegistration(
                public_profile_id=public_profile.public_profile_id,
                user_id=public_profile.user_id,
                profile_image_path=public_profile.profile_image_path,
                freelancer_intro=public_profile.freelancer_intro,
                expertise_fields=expertise_fields,
                skill_codes=skill_codes,
                educations=educations,
                careers=careers,
                sns_link=public_profile.sns_link,
                portfolios=portfolios,
                created_at=public_profile.created_at,
                updated_at=public_profile.updated_at
            )
            return FreelancerInformationDomain(complete_profile)

        def update_freelancer_intro(self, intro_text):
            result = self.repository.save_freelancer_intro(self.domain.registration.public_profile_id, intro_text)
            if result['success']:
                self.domain.update_freelancer_intro(intro_text)
                return {'success': True, 'message': '프리랜서 소개글이 성공적으로 업데이트되었습니다.'}
            return {'success': False, 'message': '프리랜서 소개글 업데이트에 실패했습니다.'}

        def update_expertise_fields(self, field_codes: list, deleted_fields: list):
            # 1. 삭제된 전문 분야 처리
            for field_code in deleted_fields:
                expertise_field = FreelancerExpertiseFieldMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    field_code=field_code
                )
                result = self.repository.delete_expertise_field(expertise_field)
                if not result['success']:
                    return {'success': False, 'message': f'{field_code} 전문 분야 삭제에 실패했습니다.'}

            # 2. 새로운 전문 분야 추가 처리
            for field_code in field_codes:
                expertise_field = FreelancerExpertiseFieldMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    field_code=field_code
                )
                result = self.repository.save_expertise_field(expertise_field)
                if not result['success']:
                    return {'success': False, 'message': f'{field_code} 전문 분야 저장에 실패했습니다.'}

            return {'success': True, 'message': '전문 분야가 성공적으로 업데이트되었습니다.'}
        
        def update_skill_codes(self, skill_codes: list, deleted_skills: list):
            # 1. 삭제된 스킬 코드 처리
            for skill_code in deleted_skills:
                skill_mapping = FreelancerSkillMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    skill_code=skill_code
                )
                result = self.repository.delete_skill_code(skill_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{skill_code} 스킬 코드 삭제에 실패했습니다.'}

            # 2. 새로운 스킬 코드 추가 처리
            for skill_code in skill_codes:
                skill_mapping = FreelancerSkillMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    skill_code=skill_code
                )
                result = self.repository.save_skill_code(skill_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{skill_code} 스킬 코드 저장에 실패했습니다.'}

            return {'success': True, 'message': '스킬 코드가 성공적으로 업데이트되었습니다.'}

        def update_educations(self, schools: list, deleted_schools: list):
            # 1. 삭제된 학력 처리
            for school in deleted_schools:
                education = FreelancerEducationMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    school=school
                )
                result = self.repository.delete_education(education)
                if not result['success']:
                    return {'success': False, 'message': f'{school} 학력 삭제에 실패했습니다.'}

            # 2. 새로운 학력 추가 처리
            for school in schools:
                education = FreelancerEducationMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    school=school
                )
                result = self.repository.save_education(education)
                if not result['success']:
                    return {'success': False, 'message': f'{school} 학력 저장에 실패했습니다.'}

            return {'success': True, 'message': '학력이 성공적으로 업데이트되었습니다.'}

        def update_careers(self, careers: list, deleted_careers: list):
            # 1. 삭제된 경력 처리
            for career_data in deleted_careers:
                career_mapping = FreelancerCareerMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    company=career_data['company'],
                    role=career_data['role'],
                    duration=career_data['duration']
                )
                result = self.repository.delete_career(career_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{career_data["company"]} 경력 삭제에 실패했습니다.'}

            # 2. 새로운 경력 추가 처리
            for career_data in careers:
                career_mapping = FreelancerCareerMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    company=career_data['company'],
                    role=career_data['role'],
                    duration=career_data['duration']
                )
                result = self.repository.save_career(career_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{career_data["company"]} 경력 저장에 실패했습니다.'}

            return {'success': True, 'message': '경력이 성공적으로 업데이트되었습니다.'}

        def update_sns_link(self, sns_link: str):
            result = self.repository.save_sns_link(self.domain.registration.public_profile_id, sns_link)
            if result['success']:
                self.domain.update_sns_link(sns_link)
                return {'success': True, 'message': 'SNS 링크가 성공적으로 저장되었습니다.'}
            return {'success': False, 'message': 'SNS 링크 저장에 실패했습니다.'}

        def change_profile_picture(self, user_id, file):
            # 유틸 함수의 create_user_folder와 일관된 경로 계산
            upload_folder = current_app.config.get('UPLOAD_FOLDER')

            # filename이 None일 경우 파일 경로 삭제 로직
            if file is None:
                # 기존 프로필 사진 경로 가져오기
                current_profile_picture = self.domain.registration.profile_image_path

                # 기존 프로필 사진이 있을 경우 삭제
                if current_profile_picture:
                    success, error = delete_image(user_id, current_profile_picture)
                    if not success:
                        return {"success": False, "message": error}
                
                # 프로필 사진 경로를 None으로 업데이트
                result = self.repository.save_profile_picture_path(self.domain.registration.public_profile_id, None)
                if result['success']:
                    self.domain.update_profile_picture_path(None)
                    return {"success": True, "message": "프로필 사진이 성공적으로 삭제되었습니다."}
                return {"success": False, "message": "프로필 사진 경로 삭제에 실패하였습니다."}

            # 파일 업로드 처리 (filename이 None이 아닐 때)
            filename, error = upload_image(file, user_id)
            if error:
                return {"success": False, "message": error}

            # 새 프로필 사진 경로 생성
            new_filepath = os.path.join(upload_folder, str(user_id), filename)

            # 기존 프로필 사진 경로 가져오기
            current_profile_picture = self.domain.registration.profile_image_path

            # 기존 프로필 사진이 있는 경우 삭제
            if current_profile_picture:
                success, error = delete_image(user_id, current_profile_picture)
                if not success:
                    return {"success": False, "message": error}

            # 새로운 프로필 사진 경로를 DB에 저장
            result = self.repository.save_profile_picture_path(self.domain.registration.public_profile_id, new_filepath)
            if result['success']:
                self.domain.update_profile_picture_path(new_filepath)
                return {"success": True, "message": "프로필 사진이 성공적으로 업데이트되었습니다."}

            return {"success": False, "message": "프로필 사진 경로 업데이트에 실패하였습니다."}
        
        def update_portfolios(self, user_id, portfolio_images: list, deleted_portfolio_images: list):
            # 1. 삭제된 포트폴리오 이미지 처리
            for image_path in deleted_portfolio_images:
                portfolio_mapping = FreelancerPortfolioMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    image_path=image_path
                )
                result = self.repository.delete_portfolio(portfolio_mapping)
                if not result['success']:
                    return {"success": False, "message": f'{image_path} 포트폴리오 이미지 삭제에 실패했습니다.'}

                # 이미지 파일도 실제로 삭제
                delete_image(user_id, image_path)

            # 2. 새로운 포트폴리오 이미지 업로드 처리
            uploaded_image_paths = []
            for file in portfolio_images:
                filename, error = upload_image(file, user_id)

                if error:
                    # 하나라도 업로드에 실패하면 이미 업로드된 파일들 삭제 후 반환
                    for uploaded_file in uploaded_image_paths:
                        delete_image(user_id, uploaded_file)  # 업로드된 이미지 삭제

                    return {"success": False, "message": f'{file.filename} 업로드에 실패했습니다. 에러: {error}'}

                # 업로드 성공 시 파일 경로 저장
                uploaded_image_paths.append(filename)

            # 모든 이미지가 성공적으로 업로드되었을 때
            for filename in uploaded_image_paths:
                portfolio_mapping = FreelancerPortfolioMapping(
                    public_profile_id=self.domain.registration.public_profile_id,
                    image_path=filename
                )
                result = self.repository.save_portfolio(portfolio_mapping)

                if not result['success']:
                    # DB 저장 중 문제가 발생하면 업로드된 파일들 삭제 후 반환
                    for uploaded_file in uploaded_image_paths:
                        delete_image(user_id, uploaded_file)

                    return {'success': False, 'message': f'{filename} 포트폴리오 이미지 저장에 실패했습니다.'}

            # 성공적으로 저장 완료된 경우
            self.domain.update_portfolio(portfolio_mapping)
            return {'success': True, 'message': '포트폴리오가 성공적으로 업데이트되었습니다.'}

        def registration_complete(self):
            # 모든 필드가 입력되었는지 확인 후 등록 완료 처리
            if all([self.domain.registration.freelancer_intro, self.domain.registration.expertise_fields, self.domain.registration.skill_codes]):
                result = update_freelancer_registration_state(self.user_id, True)
                if result['success']:
                    return {'success': True, 'message': '프리랜서 등록이 완료되었습니다.'}
            return {'success': False, 'message': '프리랜서 등록에 필요한 정보가 부족합니다.'}
