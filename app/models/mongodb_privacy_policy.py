# mongodb_privacy_policy.py

from mongoengine import Document, StringField, DateTimeField

# 개인정보 수집/이용 안내 Document 정의
class PrivacyPolicy(Document):
    version = StringField(required=True)  # 개인정보 수집/이용 안내 버전
    guide_mapping = StringField(required=True)  # 개인정보 수집/이용 안내 내용
    created_at = DateTimeField(required=True)  # 생성일

    def __str__(self):
        return f"Privacy Policy Version: {self.version}"