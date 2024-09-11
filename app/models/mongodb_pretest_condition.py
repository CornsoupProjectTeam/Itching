# mongodb_pretest_condition.py

from mongoengine import Document, StringField, IntField

# Pre-test 조건 Document 정의
class PretestCondition(Document):
    version_id = IntField(required=True, unique=True)  # 각 버전의 고유 ID
    version_name = StringField(required=True)  # 버전 이름 (예: Version 1, Version 2)
    requirements = StringField(required=True)  # 해당 버전의 요구사항 (예: "Draw a picture of a red butterfly...")

    def __str__(self):
        return f"PretestCondition Version: {self.version_name}, Requirements: {self.requirements}"