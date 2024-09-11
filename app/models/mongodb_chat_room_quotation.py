# mongodb_chat_room_quotation.py

from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField, IntField, FloatField, BooleanField

# 요구사항 Embedded Document 정의
class RequirementMapping(EmbeddedDocument):
    sequence = IntField(required=True)  # 요구사항 순서
    requirement = StringField(required=True)  # 요구사항 내용

# 알림 날짜 Embedded Document 정의
class NotificationDates(EmbeddedDocument):
    midterm_check = DateTimeField(required=True)  # 중간 점검 날짜
    final_deadline = DateTimeField(required=True)  # 제작 마감일

# 메인 ChatRoomQuotation Document 정의
class ChatRoomQuotation(Document):
    quotation_id = StringField(max_length=50, required=True)  # 견적서 ID
    chatroom_id = StringField(max_length=50,required=True, unique=True)  # 채팅방 ID
    participants = ListField(StringField(), required=True)  # 참여자 리스트
    quotation_status = StringField(required=True, choices=["drafting", "completed", "pending"])  # 견적 상태
    requirements_mapping = ListField(EmbeddedDocumentField(RequirementMapping))  # 요구사항 매핑 리스트
    quotation = FloatField(required=True)  # 견적 금액
    number_of_drafts = IntField(required=True)  # 시안 개수
    notification_dates = EmbeddedDocumentField(NotificationDates)  # 알림일 매핑
    revision_count = IntField(required=True)  # 수정 횟수
    additional_revision_purchase_available = BooleanField(default=False)  # 수정 횟수 추가 구매 가능 여부
    commercial_use_allowed = BooleanField(default=False)  # 상업적 사용 허용 여부
    high_resolution_file_available = BooleanField(default=False)  # 고해상도 파일 제공 여부
    delivery_route = StringField(required=True)  # 제공 루트
    created_at = DateTimeField(required=True)  # 생성일
    updated_at = DateTimeField(required=True)  # 수정일

    def __str__(self):
        return self.quotation_id