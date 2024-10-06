# app/domain/freelancer_list_domain.py

from enum import Enum
from datetime import datetime

# 프리랜서 등급을 나타내는 Enum 클래스
class FreelancerBadge(Enum):
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"

# 프리랜서 프로필을 나타내는 도메인 객체
class FreelancerProfile:
    def __init__(self, public_profile_id, nickname, profile_image_path, freelancer_badge, match_count, avg_response_time, registration_date, avg_rating, created_at, updated_at):
        self.public_profile_id = public_profile_id  # 고유 식별자
        self.nickname = nickname
        self.profile_image_path = profile_image_path
        self.freelancer_badge = FreelancerBadge(freelancer_badge)  # FreelancerBadge enum 사용
        self.match_count = match_count
        self.avg_response_time = avg_response_time
        self.registration_date = registration_date
        self.avg_rating = avg_rating
        self.created_at = created_at
        self.updated_at = updated_at

    # 프리랜서의 등급을 업데이트하는 메서드
    def update_badge(self, new_badge):
        if new_badge not in FreelancerBadge:
            raise ValueError("Invalid badge type")
        self.freelancer_badge = FreelancerBadge(new_badge)
        self.updated_at = datetime.utcnow()

    # 평점을 업데이트하는 메서드
    def update_rating(self, new_rating):
        if not (0 <= new_rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        self.avg_rating = new_rating
        self.updated_at = datetime.utcnow()

    # 매치 카운트를 증가시키는 메서드
    def increment_match_count(self):
        self.match_count += 1
        self.updated_at = datetime.utcnow()
