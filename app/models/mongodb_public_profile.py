# mongodb_public_profile.py

from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField, DictField, IntField, BooleanField

# 경력 Embedded Document 정의
class CareerMapping(EmbeddedDocument):
    company = StringField(required=True)  # 회사명
    role = StringField(required=True)  # 역할/직책
    duration = StringField(required=True)  # 기간

# 교육 Embedded Document 정의
class EducationMapping(EmbeddedDocument):
    school = StringField(required=True)  # 학교명
    degree = StringField(required=True)  # 학위
    graduation_year = StringField(required=True)  # 졸업연도

# 메인 PublicProfile Document 정의
class PublicProfile(Document):
    public_profile_id = StringField(max_length=30, required=True, unique=True)  # 공개 프로필 ID
    user_id = StringField(max_length=20,required=True)  # 사용자 ID
    nickname = StringField(required=True)  # 닉네임
    profile_image_path = StringField(required=True)  # 프로필 이미지 경로
    freelancer_intro = StringField(required=True)  # 프리랜서 소개
    expertise_mapping = ListField(StringField())  # 전문 분야 리스트
    skills_mapping = ListField(StringField())  # 기술 리스트
    career_mapping = ListField(EmbeddedDocumentField(CareerMapping))  # 경력 리스트
    education_mapping = ListField(EmbeddedDocumentField(EducationMapping))  # 교육 리스트
    sns_mapping = DictField()  # 소셜 네트워크 서비스(SNS) 링크
    portfolio_file_paths = ListField(StringField())  # 포트폴리오 파일 경로 리스트
    one_liner = StringField()  # 간단한 소개 문구
    project_duration = StringField()  # 프로젝트 기간
    service_options = ListField(StringField())  # 제공 서비스 옵션 리스트
    rate_unit = StringField()  # 요금 단위
    preferred_work_style_mapping = ListField(StringField())  # 선호하는 작업 스타일 리스트
    account_info = DictField()  # 계좌 정보 (은행명, 계좌 번호)
    freelancer_badge = StringField()  # 전문가 배지 (gold, silver 등)
    match_count = IntField()  # 매칭 수
    average_response_time = StringField()  # 평균 응답 시간
    freelancer_registration_date = StringField()  # 프리랜서 등록 날짜
    public_profile_registration_status = BooleanField()  # 공개 프로필 등록 상태
    created_at = DateTimeField()  # 생성일
    updated_at = DateTimeField()  # 수정일

    def __str__(self):
        return self.public_profile_id  # 공개 프로필 ID 반환
