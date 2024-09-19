# mongodb_user_information.py

from mongoengine import Document, StringField, BooleanField, DateTimeField, DictField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField, IntField, MapField
import datetime

# Mood Type의 Embedded Document 정의
class MoodType(EmbeddedDocument):
    luxurious = BooleanField(default=False)
    delicate = BooleanField(default=False)
    simple = BooleanField(default=False)
    cute = BooleanField(default=False)
    warm = BooleanField(default=False)
    smart = BooleanField(default=False)
    trendy = BooleanField(default=False)
    emotional = BooleanField(default=False)
    classic = BooleanField(default=False)

# Thumbnail Specialist의 Embedded Document 정의
class ThumbnailSpecialist(EmbeddedDocument):
    platform = MapField(BooleanField(), default={
        "YouTube": False,
        "Facebook": False,
        "KakaoStory": False,
        "Instagram": False,
        "Blog": False
    })
    design_style = MapField(BooleanField(), default={
        "Photo": False,
        "Text": False,
        "Illustration": False
    })

# Logo Specialist의 Embedded Document 정의
class LogoSpecialist(EmbeddedDocument):
    wordmark = BooleanField(default=False)
    symbol = BooleanField(default=False)
    symbol_wordmark = BooleanField(default=False)
    calligraphy = BooleanField(default=False)
    character = BooleanField(default=False)
    emblem = BooleanField(default=False)

# 선호하는 프리랜서 유형의 Embedded Document 정의
class PreferredFreelancerType(EmbeddedDocument):
    available_on_weekends = BooleanField(default=False)
    not_available_on_weekends = BooleanField(default=False)
    logo_specialist = EmbeddedDocumentField(LogoSpecialist)
    thumbnail_specialist = EmbeddedDocumentField(ThumbnailSpecialist)
    mood_type = EmbeddedDocumentField(MoodType)

# 메인 UserInformation 모델 정의
class UserInformation(Document):
    user_id = StringField(max_length=20, required=True, unique=True)
    email = StringField(max_length=50, required=True)
    profile_picture_path = StringField(max_length=255)
    nickname = StringField(max_length=20, required=True)
    business_area = StringField(max_length=100)
    
    interest_area_mapping = MapField(BooleanField(), default={
        "Thumbnail Design": False,
        "Logo Design": False
    })
    
    preferred_freelancer_type_mapping = EmbeddedDocumentField(PreferredFreelancerType)
    
    inquiry_status = BooleanField(default=False)
    freelancer_registration_status = StringField(max_length=20, required=True)
    
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.user_id