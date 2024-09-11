# mongodb_one_to_one_inquiry.py

from mongoengine import Document, StringField, DateTimeField, ListField

# 일대일 문의 Document 정의
class OneToOneInquiry(Document):
    user_id = StringField(max_length=20, required=True)  # 사용자 ID
    category = StringField(required=True)  # 문의 카테고리
    email = StringField(required=True)  # 이메일 주소
    title = StringField(required=True)  # 문의 제목
    content = StringField(required=True)  # 문의 내용
    attachment_paths = ListField(StringField())  # 첨부 파일 경로 리스트
    created_at = DateTimeField(required=True)  # 문의 생성일

    def __str__(self):
        return f"Inquiry from {self.user_id}: {self.created_at}"