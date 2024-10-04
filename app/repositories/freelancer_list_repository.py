# app/repositories/freelancer_list_repository.py

from app.models.freelancer_information import PublicProfileList  # SQLAlchemy 모델을 임포트
from app.domain.freelancer_list_domain import FreelancerProfile, FreelancerBadge
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app import db

class FreelancerProfileRepository:
    
    def find_by_id(self, public_profile_id: str) -> Optional[FreelancerProfile]:
        """주어진 ID를 통해 프리랜서 프로필을 가져옵니다."""
        try:
            profile_data = PublicProfileList.query.filter_by(public_profile_id=public_profile_id).first()
            if profile_data:
                return self._convert_to_domain(profile_data)
            return None
        except SQLAlchemyError as e:
            print(f"Error retrieving freelancer profile by ID: {e}")
            return None

    def find_all(self) -> List[FreelancerProfile]:
        """모든 프리랜서 프로필을 가져옵니다."""
        try:
            profiles_data = PublicProfileList.query.all()
            return [self._convert_to_domain(profile) for profile in profiles_data]
        except SQLAlchemyError as e:
            print(f"Error retrieving all freelancer profiles: {e}")
            return []

    def save(self, freelancer_profile: FreelancerProfile) -> bool:
        """프리랜서 프로필을 저장하거나 업데이트합니다."""
        try:
            profile_data = self._convert_to_model(freelancer_profile)
            db.session.add(profile_data)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error saving freelancer profile: {e}")
            return False

    def _convert_to_domain(self, profile_data) -> FreelancerProfile:
        """SQLAlchemy 모델 객체를 도메인 객체로 변환합니다."""
        return FreelancerProfile(
            public_profile_id=profile_data.public_profile_id,
            nickname=profile_data.nickname,
            profile_image_path=profile_data.profile_image_path,
            freelancer_badge=FreelancerBadge(profile_data.freelancer_badge),
            match_count=profile_data.match_count,
            avg_response_time=profile_data.avg_response_time,
            registration_date=profile_data.freelancer_registration_date,
            avg_rating=profile_data.average_rating,
            created_at=profile_data.created_at,
            updated_at=profile_data.updated_at
        )

    def _convert_to_model(self, freelancer_profile: FreelancerProfile):
        """도메인 객체를 SQLAlchemy 모델 객체로 변환합니다."""
        profile_data = PublicProfileList.query.filter_by(public_profile_id=freelancer_profile.public_profile_id).first()

        if not profile_data:
            profile_data = PublicProfileList(
                public_profile_id=freelancer_profile.public_profile_id,
                created_at=freelancer_profile.created_at
            )

        # 도메인 객체의 데이터를 모델 객체로 변환
        profile_data.nickname = freelancer_profile.nickname
        profile_data.profile_image_path = freelancer_profile.profile_image_path
        profile_data.freelancer_badge = freelancer_profile.freelancer_badge.value
        profile_data.match_count = freelancer_profile.match_count
        profile_data.avg_response_time = freelancer_profile.avg_response_time
        profile_data.freelancer_registration_date = freelancer_profile.registration_date
        profile_data.average_rating = freelancer_profile.avg_rating
        profile_data.updated_at = freelancer_profile.updated_at

        return profile_data
