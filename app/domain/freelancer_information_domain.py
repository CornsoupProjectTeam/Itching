from dataclasses import dataclass
from typing import List

@dataclass
class ExpertiseField:
    public_profile_id: str
    field_code: str

@dataclass
class SkillCode:
    public_profile_id: str
    skill_code: str

@dataclass
class Education:
    public_profile_id: str
    school: str

@dataclass
class Career:
    public_profile_id: str
    company: str
    role: str
    duration: int

@dataclass
class Portfolio:
    public_profile_id: str
    image_path: str

@dataclass
class FreelancerRegistration:
    public_profile_id: str
    user_id: str
    profile_image_path: str
    freelancer_intro: str
    expertise_fields: List[ExpertiseField]
    skill_codes: List[SkillCode]
    educations: List[Education]
    careers: List[Career]
    sns_link: str
    portfolios: List[Portfolio]

@dataclass
class FreelancerInformationDomain:
    registration: FreelancerRegistration

    def update_profile_picture_path(self, new_path: str):
        # 프로필 사진 경로 업데이트
        self.registration.profile_image_path = new_path

    def update_freelancer_intro(self, new_intro: str):
        # 프리랜서 소개 업데이트
        self.registration.freelancer_intro = new_intro

    def update_expertise_field(self, new_field: ExpertiseField):
        # field_code 기준 중복 확인 후 전문 분야 업데이트
        if not any(field.field_code == new_field.field_code for field in self.registration.expertise_fields):
            self.registration.expertise_fields.append(new_field)

    def update_skill_code(self, new_skill: SkillCode):
        # skill_code 기준 중복 확인 후 스킬 코드 업데이트
        if not any(skill.skill_code == new_skill.skill_code for skill in self.registration.skill_codes):
            self.registration.skill_codes.append(new_skill)

    def update_education(self, new_education: Education):
        # school 기준 중복 확인 후 학력 정보 업데이트
        if not any(education.school == new_education.school for education in self.registration.educations):
            self.registration.educations.append(new_education)

    def update_career(self, new_career: Career):
        # company와 role 기준 중복 확인 후 경력 정보 업데이트
        if not any(career.company == new_career.company and career.role == new_career.role 
                   for career in self.registration.careers):
            self.registration.careers.append(new_career)

    def update_sns_link(self, new_link: str):
        # SNS 링크 업데이트
        self.registration.sns_link = new_link

    def update_portfolio(self, new_portfolio: Portfolio):
        # image_path 기준 중복 확인 후 포트폴리오 업데이트
        if not any(portfolio.image_path == new_portfolio.image_path for portfolio in self.registration.portfolios):
            self.registration.portfolios.append(new_portfolio)