from flask import current_app
import os
from app.domain.freelancer_registration_domain import *
from app.services.user_information_service import UserInformationService
from app.repositories.user_information_repository import UserInformationRepository
from app.utils.image_upload import upload_image, delete_image
from app.utils.id_generator import generate_public_profile_id
from app.models.freelancer_information import (
    FreelancerExpertiseFieldMapping,
    FreelancerSkillMapping,
    FreelancerEducationMapping,
    FreelancerCareerMapping,
    FreelancerPortfolioMapping
)

class FreelancerRegistrationService:
    def __init__(self, freelancer_registration_repository, user_information_service, user_id):
        self.repository = freelancer_registration_repository
        self.user_information_service = user_information_service
        self.user_id = user_id
        self.domain = self.initialize_domain()

    def initialize_domain(self):
        # 공개 프로필 존재 여부 확인
        profile_check = self.repository.has_public_profile(self.user_id)
        
        if not profile_check['success']:
            # 공개 프로필이 없을 경우 닉네임을 가져와 새 프로필 생성
            nickname = self.user_information_service.get_nickname_by_user_id(self.user_id)
            
            # 닉네임이 없을 경우 에러 발생
            if not nickname:
                raise ValueError('닉네임을 찾지 못해 공개 프로필 생성이 불가능합니다.')
            
            # 새 프로필 ID 생성 및 프로필 데이터 설정
            new_profile_id = generate_public_profile_id()
            new_profile_data = {
                'public_profile_id': new_profile_id,
                'user_id': self.user_id,
                'nickname': nickname  # 닉네임을 문자열로 저장
            }
            
            # 새로운 프로필 DB에 저장
            save_result = self.repository.create_new_public_profile(new_profile_data)

            if save_result['success']:
                # 도메인 객체로 설정
                self.domain = FreelancerRegistrationDomain(
                    public_profile_id=new_profile_id,
                    user_id=self.user_id,
                    nickname=nickname,
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
            else:                
                raise ValueError('공개 프로필 생성에 실패하였습니다.')
        
        else:
            # 공개 프로필이 존재하는 경우 해당 public_profile_id로 상세 정보 가져오기
            public_profile_id = profile_check['public_profile_id']
            profile_data = self.repository.get_public_profile_for_registration(public_profile_id)
            
            if not profile_data['success']:
                return ValueError('공개 프로필을 가져오는데 실패하였습니다.')

            # 프로필과 맵핑 데이터가 있는 경우 도메인 객체 초기화
            public_profile = profile_data['profile']
            expertise_fields = profile_data.get('expertise_fields', [])
            skill_codes = profile_data.get('skill_codes', [])
            educations = profile_data.get('educations', [])
            careers = profile_data.get('careers', [])
            portfolios = profile_data.get('portfolios', [])

            # 도메인 객체에 데이터를 설정
            self.domain = FreelancerRegistrationDomain(
                public_profile_id=public_profile.public_profile_id,
                user_id=public_profile.user_id,
                nickname=public_profile.nickname,
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
        
        return self.domain

    # 프리랜서 등록 정보 조회
    def get_freelancer_registration_information(self):  
        profile = self.domain
        if profile:
            return {
                "public_profile_id": profile.public_profile_id,
                "user_id": profile.user_id,
                "profile_image_path": profile.profile_image_path,
                "freelancer_intro": profile.freelancer_intro,
                "expertise_fields": [
                    {
                        'public_profile_id': field.public_profile_id,
                        'field_code': field.field_code
                    } for field in profile.expertise_fields
                ],
                "skill_codes": [
                    {
                        'public_profile_id': skill.public_profile_id,
                        'skill_code': skill.skill_code
                    } for skill in profile.skill_codes
                ],
                "educations": [
                    {
                        'sequence': education.sequence,
                        'public_profile_id': education.public_profile_id,
                        'school': education.school
                    } for education in profile.educations
                ],
                "careers": [
                    {
                        'sequence': career.sequence,
                        'public_profile_id': career.public_profile_id,
                        'company': career.company,
                        'role': career.role,
                        'duration': career.duration
                    } for career in profile.careers
                ],
                "portfolios": [
                    {
                        'sequence': portfolio.sequence,
                        'public_profile_id': portfolio.public_profile_id,
                        'image_path': portfolio.image_path
                    } for portfolio in profile.portfolios
                ],
                "sns_link": profile.sns_link,
                "created_at": profile.created_at,
                "updated_at": profile.updated_at
            }
        else:
            return None
        
    def update_freelancer_intro(self, user_id, intro_text):
        result = self.repository.save_freelancer_intro(self.domain.public_profile_id, intro_text)
        if result['success']:
            self.domain.update_freelancer_intro(intro_text)
            return {'success': True, 'message': '프리랜서 소개글이 성공적으로 업데이트되었습니다.'}
        return {'success': False, 'message': '프리랜서 소개글 업데이트에 실패했습니다.'}

    def update_expertise_fields(self, user_id, field_codes: Optional[list], deleted_field_codes: Optional[list]):
        # 새로운 전문 분야 추가 처리
        if field_codes:
            for field_code in field_codes:
                expertise_field = FreelancerExpertiseFieldMapping(
                    public_profile_id=self.domain.public_profile_id,
                    field_code=field_code
                )
                result = self.repository.save_expertise_field(expertise_field)
                if not result['success']:
                    return {'success': False, 'message': f'{field_code} 전문 분야 저장에 실패했습니다.'}
                self.domain.update_expertise_field(expertise_field)

        # 삭제된 전문 분야 처리
        if deleted_field_codes:
            for field_code in deleted_field_codes:
                expertise_field = FreelancerExpertiseFieldMapping(
                    public_profile_id=self.domain.public_profile_id,
                    field_code=field_code
                )
                result = self.repository.delete_expertise_field(expertise_field)
                if not result['success']:
                    return {'success': False, 'message': f'{field_code} 전문 분야 삭제에 실패했습니다.'}
                self.domain.remove_expertise_field_code(expertise_field)

        return {'success': True, 'message': '전문 분야가 성공적으로 업데이트되었습니다.'}

    def update_skill_codes(self, user_id, skill_codes: Optional[list], deleted_skill_codes: Optional[list]):
        # 새로운 스킬 코드 추가 처리
        if skill_codes:
            for skill_code in skill_codes:
                skill_mapping = FreelancerSkillMapping(
                    public_profile_id=self.domain.public_profile_id,
                    skill_code=skill_code
                )
                result = self.repository.save_skill_code(skill_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{skill_code} 스킬 코드 저장에 실패했습니다.'}
                self.domain.update_skill_code(skill_mapping)
        
        # 삭제된 스킬 코드 처리
        if deleted_skill_codes:
            for skill_code in deleted_skill_codes:
                skill_mapping = FreelancerSkillMapping(
                    public_profile_id=self.domain.public_profile_id,
                    skill_code=skill_code
                )
                result = self.repository.delete_skill_code(skill_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{skill_code} 스킬 코드 삭제에 실패했습니다.'}
                self.domain.remove_skill_code(skill_mapping)
        
        return {'success': True, 'message': '스킬 코드가 성공적으로 업데이트되었습니다.'}

    def update_educations(self, user_id, schools: list, deleted_schools: list):
        # 새로운 학력 추가 처리
        if schools:
            for school in schools:
                education = FreelancerEducationMapping(
                    public_profile_id=self.domain.public_profile_id,
                    school=school
                )
                result = self.repository.save_education(education)
                if not result['success']:
                    return {'success': False, 'message': f'{school} 학력 저장에 실패했습니다.'}
                self.domain.update_education(education)

        # 삭제된 학력 처리
        if deleted_schools:
            for school in deleted_schools:
                education = FreelancerEducationMapping(
                    public_profile_id=self.domain.public_profile_id,
                    school=school
                )
                result = self.repository.delete_education(education)
                if not result['success']:
                    return {'success': False, 'message': f'{school} 학력 삭제에 실패했습니다.'}
                self.domain.remove_education(education)

        return {'success': True, 'message': '학력이 성공적으로 업데이트되었습니다.'}

    def update_careers(self, user_id, careers: list, deleted_careers: list):
        # 새로운 경력 추가 처리
        if careers:
            for career_data in careers:
                career_mapping = FreelancerCareerMapping(
                    public_profile_id=self.domain.public_profile_id,
                    company=career_data['company'],
                    role=career_data['role'],
                    duration=career_data['duration']
                )
                result = self.repository.save_career(career_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{career_data["company"]} 경력 저장에 실패했습니다.'}
                self.domain.update_career(career_mapping)

        # 삭제된 경력 처리
        if deleted_careers:
            for career_data in deleted_careers:
                career_mapping = FreelancerCareerMapping(
                    public_profile_id=self.domain.public_profile_id,
                    company=career_data['company'],
                    role=career_data['role'],
                    duration=career_data['duration']
                )
                result = self.repository.delete_career(career_mapping)
                if not result['success']:
                    return {'success': False, 'message': f'{career_data["company"]} 경력 삭제에 실패했습니다.'}
                self.domain.remove_career(career_mapping)

        return {'success': True, 'message': '경력이 성공적으로 업데이트되었습니다.'}

    def update_sns_link(self, user_id, sns_link: str):
        result = self.repository.save_sns_link(self.domain.public_profile_id, sns_link)
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
            current_profile_picture = self.domain.profile_image_path

            # 기존 프로필 사진이 있을 경우 삭제
            if current_profile_picture:
                success, error = delete_image(user_id, current_profile_picture)
                if not success:
                    return {"success": False, "message": error}
            
            # 프로필 사진 경로를 None으로 업데이트
            result = self.repository.save_profile_picture_path(self.domain.public_profile_id, None)
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
        current_profile_picture = self.domain.profile_image_path

        # 기존 프로필 사진이 있는 경우 삭제
        if current_profile_picture:
            success, error = delete_image(user_id, current_profile_picture)
            if not success:
                return {"success": False, "message": error}

        # 새로운 프로필 사진 경로를 DB에 저장
        result = self.repository.save_profile_picture_path(self.domain.public_profile_id, new_filepath)
        if result['success']:
            self.domain.update_profile_picture_path(new_filepath)
            return {"success": True, "message": "프로필 사진이 성공적으로 업데이트되었습니다."}

        return {"success": False, "message": "프로필 사진 경로 업데이트에 실패하였습니다."}
    
    def update_portfolios(self, user_id, portfolio_images: list, deleted_portfolio_image_paths: list):        
        # 1. 삭제된 포트폴리오 이미지 처리
        if deleted_portfolio_image_paths:
            for image_path in deleted_portfolio_image_paths:
                portfolio_mapping = FreelancerPortfolioMapping(
                    public_profile_id=self.domain.public_profile_id,
                    image_path=image_path
                )
                result = self.repository.delete_portfolio(portfolio_mapping)
                if not result['success']:
                    return {"success": False, "message": f'{image_path} 포트폴리오 이미지 삭제에 실패했습니다.'}

                # 이미지 파일도 실제로 삭제
                delete_image(user_id, image_path)

                self.domain.remove_portfolio_path(portfolio_mapping)

            # 삭제 작업이 성공적으로 수행되었을 때 메시지 반환
            return {'success': True, 'message': '포트폴리오 이미지가 성공적으로 삭제되었습니다.'}

        # 2. 새로운 포트폴리오 이미지 업로드 처리
        uploaded_image_paths = []    

        if portfolio_images:
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
                    public_profile_id=self.domain.public_profile_id,
                    image_path=filename
                )
                result = self.repository.save_portfolio(portfolio_mapping)

                if not result['success']:
                    # DB 저장 중 문제가 발생하면 업로드된 파일들 삭제 후 반환
                    for uploaded_file in uploaded_image_paths:
                        delete_image(user_id, uploaded_image_paths)

                    return {'success': False, 'message': f'{filename} 포트폴리오 이미지 저장에 실패했습니다.'}

            # 모든 포트폴리오가 성공적으로 DB에 저장된 경우에만 도메인 객체 업데이트
            if uploaded_image_paths:
                
                self.domain.update_portfolio(portfolio_mapping)
                return {'success': True, 'message': '포트폴리오가 성공적으로 업데이트되었습니다.'}
        
        # 만약 portfolio_images와 deleted_portfolio_image_paths 모두 없으면 에러 메시지 반환
        return {'success': False, 'message': '포트폴리오 이미지나 삭제할 포트폴리오가 제공되지 않았습니다.'}

    def registration_complete(self, user_id):
        profile = self.domain
        
        # 필수 필드가 채워져 있는지 확인
        required_fields = [
            profile.nickname,
            profile.freelancer_intro,
            profile.expertise_fields,
            profile.skill_codes,
            profile.educations,
            profile.careers
        ]
        
        # 필수 필드 중 하나라도 비어 있다면 False를 반환
        if any(field is None or (isinstance(field, list) and not field) for field in required_fields):
            return {
                "success": False,
                "message": "필수 등록 정보가 누락되었습니다."
            }
        
        # 모든 필수 필드가 채워진 경우 모든 정보를 반환
        return {
            "success": True,
            "message": "모든 필수 등록 정보가 완료되었습니다.",
            "data": {
                "public_profile_id": profile.public_profile_id,
                "user_id": profile.user_id,
                "profile_image_path": profile.profile_image_path,
                "freelancer_intro": profile.freelancer_intro,
                "expertise_fields": [
                    {
                        'public_profile_id': field.public_profile_id,
                        'field_code': field.field_code
                    } for field in profile.expertise_fields
                ],
                "skill_codes": [
                    {
                        'public_profile_id': skill.public_profile_id,
                        'skill_code': skill.skill_code
                    } for skill in profile.skill_codes
                ],
                "educations": [
                    {
                        'sequence': education.sequence,
                        'public_profile_id': education.public_profile_id,
                        'school': education.school
                    } for education in profile.educations
                ],
                "careers": [
                    {
                        'sequence': career.sequence,
                        'public_profile_id': career.public_profile_id,
                        'company': career.company,
                        'role': career.role,
                        'duration': career.duration
                    } for career in profile.careers  # 여기서 딕셔너리로 변환
                ],
                "portfolios": [
                    {
                        'sequence': portfolio.sequence,
                        'public_profile_id': portfolio.public_profile_id,
                        'image_path': portfolio.image_path
                    } for portfolio in profile.portfolios
                ],
                "sns_link": profile.sns_link,
                "created_at": profile.created_at,
                "updated_at": profile.updated_at
            }
        }

