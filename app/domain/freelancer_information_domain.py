from dataclasses import dataclass,field
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Numeric, Enum
from app.models.freelancer_information import (
    FreelancerServiceOptions,
    FreelancerPriceRange,
    PreferredWorkStyleMapping,
    FreelancerAccountInfo,
    Review,
    ReviewSummary
)

@dataclass
class FreelancerInformationDomain:
    # 프리랜서 확인 정보
    freelancer_badge: Optional[str] = None
    match_count: int = None
    review: List['Review'] = field(default_factory=list)
    review_summary: List['ReviewSummary'] = field(default_factory=list)

    # 프리랜서 추가 정보 입력
    freelancer_intro_one_liner: Optional[str] = None
    project_duration: Optional[int] = None
    service_options: List['FreelancerServiceOptions'] = field(default_factory=list)
    price_range: List['FreelancerPriceRange'] = field(default_factory=list)
    preferred_work_style: List['PreferredWorkStyleMapping'] = field(default_factory=list)
    account_info: List['FreelancerAccountInfo'] = field(default_factory=list)
    
    # 프리랜서 등록 상태
    public_profile_registration_st: bool = None

    # 프로젝트 기간 업데이트
    def update_project_duration(self, project_duration):
        self.project_duration = project_duration

    # 공개 프로필 등록 상태 업데이트
    def update_public_profile_registration_st(self, registration_status):
        self.public_profile_registration_st = registration_status

    # 프리랜서 소개 한 줄 업데이트
    def update_freelancer_intro_one_liner(self, intro_one_liner):
        self.freelancer_intro_one_liner = intro_one_liner
    
        # 서비스 옵션 업데이트
    def update_service_options(self, weekend_consultation, weekend_work):
        self.service_options.weekend_consultation = weekend_consultation
        self.service_options.weekend_work = weekend_work

    # 가격 범위 업데이트
    def update_price_range(self, min_price, max_price, price_unit):
        self.price_range.min_price = min_price
        self.price_range.max_price = max_price
        self.price_range.price_unit = price_unit

    # 계정 정보 업데이트
    def update_account_info(self, bank_name, account_number, account_holder, account_type):
        self.account_info.bank_name = bank_name
        self.account_info.account_number = account_number
        self.account_info.account_holder = account_holder
        self.account_info.account_type = account_type

    # 선호 업무 스타일 추가
    def add_preferred_work_style(self, new_style: PreferredWorkStyleMapping):
        if not any(style.preferred_code == new_style.preferred_code for style in self.preferred_work_style):
            self.preferred_work_style.append(new_style)

    # 선호 업무 스타일 삭제
    def remove_preferred_work_style(self, preferred_style: PreferredWorkStyleMapping):
        to_remove = [style for style in self.preferred_work_style if style.preferred_code == preferred_style.preferred_code]

        for style in to_remove:
            if style in self.preferred_work_style:
                self.preferred_work_style.remove(style)
            else:
                print(f"오류: {style.preferred_code}가 선호 업무 스타일에서 찾을 수 없습니다.")
                
    # 리뷰 추가
    def add_review(self, review: Review):
        # 중복 확인 후 리뷰 추가
        if not any(r.sequence == review.sequence for r in self.review):
            self.review.append(review)

    # 리뷰 삭제
    def remove_review(self, review: Review):
        # 일치하는 리뷰를 도메인 객체에서 삭제
        self.review = [r for r in self.review if r.sequence != review.sequence]

    # 리뷰 요약 업데이트
    def update_review_summary(self, total_reviews: int, average_rating: float):
        if self.review_summary:
            # 기존 리뷰 요약 업데이트
            self.review_summary.total_reviews = total_reviews
            self.review_summary.average_rating = average_rating
        else:
            # 리뷰 요약이 없을 경우 생성
            self.review_summary = ReviewSummary(
                public_profile_id=self.public_profile_id,
                total_reviews=total_reviews,
                average_rating=average_rating
            )

# 도메인 필요 없으나 개발 편의를 위해 작성해둠 나중에 삭제
# class PublicProfileList:
#     public_profile_id: str
#     nickname: str
#     profile_image_path: Optional[str] # 프리랜서 등록에서 변경 같이 하도록 추가
#     freelancer_badge: Optional[str] # 나중에 도연이 스캐너 개발된 후에 결정
#     match_count: int # 서비스는 프리랜서 정보에 있고 채팅방 추가될 때마다 업데이트되도록
#     #average_response_time: Optional[int]
#     freelancer_registration_date: Optional[datetime]
#     average_rating: Numeric # 리뷰 테이블 업데이트 될때마다 변경되도록
#     created_at: datetime
#     updated_at: datetime