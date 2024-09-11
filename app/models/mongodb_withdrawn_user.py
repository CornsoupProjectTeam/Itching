# mongodb_withdrawn_user.py

from mongoengine import Document, StringField, DateTimeField, DictField
import datetime

# 탈퇴 회원 Document 정의
class WithdrawnUser(Document):
    user_id = StringField(max_length=20, required=True, unique=True)  # 사용자 ID
    withdrawal_data_mapping = DictField()  # 탈퇴 회원의 데이터 매핑 (기존 데이터에서 변환된 형식으로 저장)
    created_at = DateTimeField(default=datetime.datetime.utcnow)  # 탈퇴 데이터 생성일
    updated_at = DateTimeField(default=datetime.datetime.utcnow)  # 탈퇴 데이터 수정일

    def __str__(self):
        return self.user_id