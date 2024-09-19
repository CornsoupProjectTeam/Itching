import os
from pymongo import MongoClient
from datetime import datetime

# 환경변수에서 Mongo URI 가져오기
mongo_uri = os.getenv('MONGO_URI')

# MongoDB 클라이언트 설정
client = MongoClient(mongo_uri)
db = client['itching_mongodb'] 
collection = db['user_information']

# 삽입할 데이터
user_data = {
    "user_id": "ujin6666",
    "email": "ujin736@gmail.com",
    "profile_picture_path": "/images/profiles/user123.jpg",
    "nickname": "chobob",
    "business_area": "Marketing and Advertising",
    "interest_area_mapping": {
        "Thumbnail Design": True,
        "Logo Design": False
    },
    "preferred_freelancer_type_mapping": {
        "available_on_weekends": True,  # 필드명 수정
        "not_available_on_weekends": False,  # 필드명 수정
        "logo_specialist": {  # 필드명 수정
            "wordmark": False,  # 필드명 수정
            "symbol": True,  # 필드명 수정
            "symbol_wordmark": True,  # 필드명 수정
            "calligraphy": False,
            "character": False,
            "emblem": False
        },
        "thumbnail_specialist": {  # 필드명 수정
            "platform": {
                "YouTube": True,
                "Facebook": False,
                "KakaoStory": False,
                "Instagram": True,
                "Blog": False
            },
            "design_style": {  # 필드명 수정
                "Photo": True,
                "Text": False,
                "Illustration": True
            }
        },
        "mood_type": {  # 필드명 수정
            "luxurious": False,
            "delicate": True,
            "simple": True,
            "cute": False,
            "warm": True,
            "smart": False,
            "trendy": False,
            "emotional": False,
            "classic": False
        }
    },
    "inquiry_status": True,
    "freelancer_registration_status": True,
    "created_at": datetime.utcnow(),  # 현재 시간으로 생성
    "updated_at": datetime.utcnow()  # 현재 시간으로 업데이트
}


# 데이터 삽입
result = collection.insert_one(user_data)
print(f"Inserted document with _id: {result.inserted_id}")
