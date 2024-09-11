# mongodb_project_info.py

from mongoengine import Document, StringField, DateTimeField, ListField, IntField, FloatField, BooleanField

# 메인 ProjectInfo Document 정의
class ProjectInfo(Document):
    project_id = IntField(max_length=50,required=True, unique=True)  # 프로젝트 ID
    public_profile_id = StringField(max_length=30, required=True)  # 공개 프로필 ID
    category_mapping = ListField(StringField())  # 분야 매핑 리스트
    image_path_mapping = ListField(StringField())  # 이미지 경로 리스트
    project_title = StringField(required=True)  # 프로젝트 제목
    project_payment_amount = IntField(required=True)  # 프로젝트 비용
    revision_count = IntField(required=True)  # 수정 횟수
    additional_revision_available = BooleanField(default=False)  # 추가 수정 가능 여부
    production_time = StringField(required=True)  # 제작 기간
    commercial_use_allowed = BooleanField(default=False)  # 상업적 사용 허용 여부
    high_resolution_file_available = BooleanField(default=False)  # 고해상도 파일 제공 여부
    delivery_routes = ListField(StringField())  # 파일 전달 방법 리스트
    additional_notes = StringField()  # 추가 메모
    cancellation_and_refund_policy = StringField()  # 취소 및 환불 정책
    product_info_disclosure = StringField()  # 제품 정보 공개
    additional_info = StringField()  # 추가 정보
    created_at = DateTimeField(required=True)  # 생성일
    updated_at = DateTimeField(required=True)  # 수정일

    def __str__(self):
        return self.project_id