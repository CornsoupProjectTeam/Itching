# mongodb_service_terms.py

from mongoengine import Document, StringField, DateTimeField

# 서비스 이용 약관 Document 정의
class ServiceTerms(Document):
    version = StringField(required=True)  # 서비스 약관 버전
    terms_mapping = StringField(required=True)  # 약관 내용
    created_at = DateTimeField(required=True)  # 생성일

    def __str__(self):
        return f"Service Terms Version: {self.version}"