import os
from pymongo import MongoClient
from datetime import datetime

# 환경변수에서 Mongo URI 가져오기
mongo_uri = os.getenv('MONGO_URI')

# MongoDB 클라이언트 설정
client = MongoClient(mongo_uri)
db = client['itching_mongodb'] 
collection = db['chat_room_quotation']

# 삽입할 데이터
user_data = {
  "chatroom_id_abc123": {
    "estimate_id": "estimate_id_67890",
    "participants": [
      "user_id_123",
      "user_id_456"
    ],
    "estimate_status": "drafting",
    "requirements_mapping": [
      {
        "sequence": 1,
        "requirement": "Design a logo for a new brand"
      },
      {
        "sequence": 2,
        "requirement": "Create a color palette"
      }
    ],
    "estimate": 500,
    "number_of_drafts": 3,
    "notification_dates": {
      "midterm_check": "2024-08-10T10:00:00Z",
      "final_deadline": "2024-08-20T10:00:00Z"
    },
    "revision_count": 2,
    "additional_revision_purchase_available": True,
    "commercial_use_allowed": True,
    "high_resolution_file_available": True,
    "delivery_method": "email",
    "created_at": "2024-08-06T12:34:56Z",
    "updated_at": "2024-08-07T14:00:00Z"
  },
  "chatroom_id_def456": {
    "estimate_id": "estimate_id_12345",
    "participants": [
      "user_id_321",
      "user_id_654"
    ],
    "estimate_status": "drafting",
    "requirements_mapping": [
      {
        "sequence": 1,
        "requirement": "Develop a homepage"
      },
      {
        "sequence": 2,
        "requirement": "Set up an e-commerce section"
      }
    ],
    "estimate": 1500,
    "number_of_drafts": 5,
    "notification_dates": {
      "midterm_check": "2024-08-11T15:00:00Z",
      "final_deadline": "2024-08-21T15:00:00Z"
    },
    "revision_count": 3,
    "additional_revision_purchase_available": False,
    "commercial_use_allowed": True,
    "high_resolution_file_available": False,
    "delivery_method": "online platform",
    "created_at": "2024-08-05T09:20:00Z",
    "updated_at": "2024-08-06T11:30:00Z"
  }
}



# 데이터 삽입
result = collection.insert_one(user_data)
print(f"Inserted document with _id: {result.inserted_id}")