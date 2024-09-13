# mongodb_user_recommendation.py

from mongoengine import Document, StringField, DateTimeField, ListField, FloatField, EmbeddedDocument, EmbeddedDocumentField

# 추천 정보 Embedded Document 정의
class RecommendationMapping(EmbeddedDocument):
    post_id = StringField(max_length=50, required=True)  # 글 ID
    category = StringField(required=True, choices=["project", "freelancer", "client"])  # 카테고리 (프로젝트, 프리랜서, 클라이언트)
    score = FloatField(required=True)  # 추천 점수
    created_at = DateTimeField(required=True)  # 추천 생성일
    updated_at = DateTimeField(required=True)  # 추천 수정일

# 메인 UserRecommendation Document 정의
class UserRecommendation(Document):
    user_id = StringField(max_length=20,required=True, unique=True)  # 유저 ID
    recommendation_mapping = ListField(EmbeddedDocumentField(RecommendationMapping))  # 추천 정보 리스트

    def __str__(self):
        return f"User Recommendations for {self.user_id}"