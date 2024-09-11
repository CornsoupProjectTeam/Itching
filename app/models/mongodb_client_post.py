# mongodb_client_post.py

from mongoengine import Document, StringField, DateTimeField, ListField, IntField

# 메인 ClientPost Document 정의
class ClientPost(Document):
    client_post_id = IntField(max_length=50, required=True, unique=True)  # 클라이언트 글 ID
    client_user_id = StringField(max_length=20,required=True)  # 클라이언트 유저 ID
    field = StringField(required=True)  # 작업 분야 (예: 로고, 썸네일)
    client_title = StringField(required=True)  # 클라이언트 글 제목
    client_payment_amount = IntField(required=True)  # 클라이언트 지불 금액
    desired_deadline = DateTimeField(required=True)  # 희망 마감일
    final_deadline = DateTimeField(required=True)  # 최종 마감일
    requirements = StringField(required=True)  # 요구사항
    reference_paths = ListField(StringField())  # 참고 자료 경로 리스트
    created_at = DateTimeField(required=True)  # 글 생성일
    updated_at = DateTimeField(required=True)  # 글 수정일

    def __str__(self):
        return self.client_post_id