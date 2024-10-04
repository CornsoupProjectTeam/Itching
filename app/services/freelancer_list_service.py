# app/services/freelancer_list_service.py

from app.repositories.freelancer_list_repository import FreelancerProfileRepository
from typing import List, Optional
from app.domain.freelancer_list_domain import FreelancerProfile

class FreelancerProfileService:
    def __init__(self, freelancer_repository: FreelancerProfileRepository):
        self.freelancer_repository = freelancer_repository

    def get_freelancer_by_id(self, public_profile_id: str) -> Optional[FreelancerProfile]:
        """특정 프리랜서 프로필을 ID로 가져옵니다."""
        return self.freelancer_repository.find_by_id(public_profile_id)

    def get_all_freelancers(self) -> List[FreelancerProfile]:
        """모든 프리랜서 프로필을 가져옵니다."""
        return self.freelancer_repository.find_all()

    def save_freelancer(self, freelancer_profile: FreelancerProfile) -> bool:
        """프리랜서 프로필을 저장합니다."""
        return self.freelancer_repository.save(freelancer_profile)
