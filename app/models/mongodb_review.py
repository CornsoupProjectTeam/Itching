# mongodb_review.py

from mongoengine import Document, StringField, DateTimeField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField

# 리뷰 Embedded Document 정의
class ReviewMapping(EmbeddedDocument):
    review_title = StringField(required=True)  # 리뷰 제목
    client_user_id = StringField(max_length=20, required=True)  # 클라이언트 유저 ID
    rating = FloatField(required=True)  # 별점
    review = StringField(required=True)  # 리뷰 내용
    attachment_paths = ListField(StringField())  # 첨부 파일 경로 리스트
    created_at = DateTimeField(required=True)  # 리뷰 생성일

# 메인 Review Document 정의
class Review(Document):
    freelancer_user_id = StringField(max_length=20,required=True)  # 프리랜서 유저 ID
    public_profile_id = StringField(max_length=30,required=True)  # 공개 프로필 ID
    review_mapping = ListField(EmbeddedDocumentField(ReviewMapping))  # 리뷰 리스트
    average_rating = FloatField(required=True)  # 평균 별점
    created_at = DateTimeField(required=True)  # 리뷰 컬렉션 생성일
    updated_at = DateTimeField(required=True)  # 리뷰 컬렉션 수정일

    def __str__(self):
        return f"Freelancer: {self.freelancer_user_id}, Average Rating: {self.average_rating}"