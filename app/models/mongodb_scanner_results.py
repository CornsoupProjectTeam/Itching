# mongodb_scanner_result.py

from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField, IntField, FloatField

# 스캔 세부 정보 Embedded Document 정의
class ScanDetail(EmbeddedDocument):
    result = StringField(required=True, default="Passed")  # 스캔 결과 (예: Passed, Failed)
    score = IntField(required=True)  # 스캔 점수
    created_at = DateTimeField(required=True)  # 스캔이 완료된 시각

# 스캔 시퀀스 Embedded Document 정의
class ScanResult(EmbeddedDocument):
    sequence = IntField(required=True)  # 시퀀스 번호
    requirements = ListField(StringField(), required=True)  # 각 시퀀스의 요구사항 리스트
    scan_details = ListField(EmbeddedDocumentField(ScanDetail))  # 스캔 세부 정보 리스트

# 메인 ScannerResults Document 정의
class ScannerResults(Document):
    type = StringField(required=True, choices=["chat_room", "pre-test"])  # 스캐너 타입 (chat_room 또는 pre-test)
    
    # 채팅방 스캐너 필드
    quotation_id = StringField(max_length=50)  # 채팅방 스캐너의 경우: 견적서 ID
    # Pre-test 스캐너 필드
    user_id = StringField(max_length=20)  # Pre-test 스캐너의 경우: 사용자 ID
    version_id = IntField()  # Pre-test 스캐너의 경우: 사용된 조건 버전 ID
    
    # 공통 필드
    image_path = StringField(required=True)  # 이미지 경로
    created_at = DateTimeField(required=True)  # 생성일
    scan_results = ListField(EmbeddedDocumentField(ScanResult))  # 스캔 결과 리스트
    average_score = FloatField(required=True)  # 평균 점수

    def __str__(self):
        return f"ScannerResult Type: {self.type}, ID: {self.quotation_id or self.user_id}"
