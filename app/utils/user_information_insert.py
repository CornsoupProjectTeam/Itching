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
        "Available on Weekends": True,
        "Not Available on Weekends": False,
        "Logo Specialist": {
            "Wordmark": False,
            "Symbol": True,
            "Symbol + Wordmark": True,
            "Calligraphy": False,
            "Character": False,
            "Emblem": False
        },
        "Thumbnail Specialist": {
            "Platform": {
                "YouTube": True,
                "Facebook": False,
                "KakaoStory": False,
                "Instagram": True,
                "Blog": False
            },
            "Design Style": {
                "Photo": True,
                "Text": False,
                "Illustration": True
            }
        },
        "Mood Type": {
            "Luxurious": False,
            "Delicate": True,
            "Simple": True,
            "Cute": False,
            "Warm": True,
            "Smart": False,
            "Trendy": False,
            "Emotional": False,
            "Classic": False
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
