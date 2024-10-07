from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from app.models.freelancer_information import (
    FreelancerExpertiseFieldMapping,
    FreelancerSkillMapping,
    FreelancerEducationMapping,
    FreelancerCareerMapping,
    FreelancerPortfolioMapping
)

@dataclass
class FreelancerRegistrationDomain:
    public_profile_id: str
    user_id: str
    nickname: str
    profile_image_path: Optional[str] = None
    freelancer_intro: Optional[str] = None
    expertise_fields: List['FreelancerExpertiseFieldMapping'] = None
    skill_codes: List['FreelancerSkillMapping'] = None
    educations: List['FreelancerEducationMapping'] = None
    careers: List['FreelancerCareerMapping'] = None
    sns_link: Optional[str] = None
    portfolios: List['FreelancerPortfolioMapping'] = None
    freelancer_registration_date: Optional[datetime] = None
    freelancer_badge: Optional[str] = None

    def update_profile_picture_path(self, new_path: str):
        # 프로필 사진 경로 업데이트
        self.profile_image_path = new_path

    def update_freelancer_intro(self, new_intro: str):
        # 프리랜서 소개 업데이트
        self.freelancer_intro = new_intro

    def update_expertise_field(self, new_field: FreelancerExpertiseFieldMapping):
        # field_code 기준 중복 확인 후 전문 분야 업데이트
        if not any(field.field_code == new_field.field_code for field in self.expertise_fields):
            self.expertise_fields.append(new_field)

    def remove_expertise_field_code(self, expertise_field_mapping: FreelancerExpertiseFieldMapping):
        # 주어진 매핑에 해당하는 전문 분야를 도메인 객체에서 삭제
        to_remove = [field for field in self.expertise_fields if field.field_code == expertise_field_mapping.field_code]

        for field in to_remove:
            if field in self.expertise_fields:
                self.expertise_fields.remove(field)
            else:
                print(f"오류: {field.field_code}가 전문 분야에서 찾을 수 없습니다.")

    def update_skill_code(self, new_skill: FreelancerSkillMapping):
        # skill_code 기준 중복 확인 후 스킬 코드 업데이트
        if not any(skill.skill_code == new_skill.skill_code for skill in self.skill_codes):
            self.skill_codes.append(new_skill)

    def remove_skill_code(self, skill_mapping: FreelancerSkillMapping):
        # 주어진 매핑에 해당하는 스킬 코드를 도메인 객체에서 삭제
        to_remove = [skill for skill in self.skill_codes if skill.skill_code == skill_mapping.skill_code]

        for skill in to_remove:
            if skill in self.skill_codes:
                self.skill_codes.remove(skill)
            else:
                print(f"오류: {skill.skill_code}가 스킬 코드 리스트에서 찾을 수 없습니다.")

    def update_education(self, new_education: FreelancerEducationMapping):
        # school 기준 중복 확인 후 학력 정보 업데이트
        if not any(education.school == new_education.school for education in self.educations):
            self.educations.append(new_education)

    def remove_education(self, education_mapping: FreelancerEducationMapping):
        # 주어진 매핑에 해당하는 학력을 도메인 객체에서 삭제
        to_remove = [education for education in self.educations if education.school == education_mapping.school]

        for education in to_remove:
            if education in self.educations:
                self.educations.remove(education)
            else:
                print(f"오류: {education.school} 학력을 찾을 수 없습니다.")

    def update_career(self, new_career: FreelancerCareerMapping):
        # company와 role 기준 중복 확인 후 경력 정보 업데이트
        if not any(career.company == new_career.company and career.role == new_career.role 
                   for career in self.careers):
            self.careers.append(new_career)

    def remove_career(self, career_mapping: FreelancerCareerMapping):
        # 주어진 매핑에 해당하는 경력을 도메인 객체에서 삭제
        to_remove = [career for career in self.careers if career.company == career_mapping.company and career.role == career_mapping.role]

        for career in to_remove:
            if career in self.careers:
                self.careers.remove(career)
            else:
                print(f"오류: {career.company}에서 {career.role} 역할을 가진 경력을 찾을 수 없습니다.")

    def update_sns_link(self, new_link: str):
        # SNS 링크 업데이트
        self.sns_link = new_link

    def update_portfolio(self, new_portfolio: FreelancerPortfolioMapping):
        # image_path 기준 중복 확인 후 포트폴리오 업데이트
        if not any(portfolio.image_path == new_portfolio.image_path for portfolio in self.portfolios):
            self.portfolios.append(new_portfolio)
    
    def remove_portfolio_path(self, portfolio_mapping: FreelancerPortfolioMapping):
        # 주어진 매핑에 해당하는 포트폴리오 이미지를 도메인 객체에서 삭제
        to_remove = [portfolio for portfolio in self.portfolios if portfolio.image_path == portfolio_mapping.image_path]

        for portfolio in to_remove:
            if portfolio in self.portfolios:
                self.portfolios.remove(portfolio)
            else:
                print(f"오류: {portfolio.image_path} 포트폴리오 이미지를 찾을 수 없습니다.")
    
    def update_registration_date(self, registration_date:datetime):
        # 프리랜서 등록일 업데이트
        self.freelancer_registration_date = registration_date