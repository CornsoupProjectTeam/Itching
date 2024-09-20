import os
from pymongo import MongoClient
from datetime import datetime

# 환경변수에서 Mongo URI 가져오기
mongo_uri = os.getenv('MONGO_URI')

# MongoDB 클라이언트 설정
client = MongoClient(mongo_uri)
db = client['itching_mongodb'] 
collection = db['quotation']

# 삽입할 데이터
user_data = {
  "chat_room_id": 12345,
  "participants_mapping": {
    "freelancer_user_id": "freelancer01",
    "client_user_id": "client02"
  },  
  "support_language_mapping": {
    "freelancer_language": "English",
    "client_language": "Korean"
  },  
  "pin_status_mapping": {
    "freelancer01": True,  
    "client02": False 
  },  
  "message_mapping": [
    {
      "sender_user_id": "freelancer01", 
      "message_content": "Hello!",  
      "status": "read",  
      "created_at": "2024-01-01T12:00:00Z" 
    },
    {
      "sender_user_id": "client02",  
      "message_content": "해당 프로젝트에 관심이 있으신가요",  
      "status": "read",  
      "created_at": "2024-01-01T12:10:00Z"  
    }
  ],  
  "is_new_notification": False, 
  "blocked_users": [
    {
      "blocker_user_id": "client_id_002",  
      "blocked_user_id": "freelancer_id_001",  
      "blocked_at": "2024-01-02T09:00:00Z"  
    }
  ],  
  "created_at": "2024-01-01T12:00:00Z", 
  "updated_at": "2024-01-02T14:00:00Z"  
}


# 데이터 삽입
result = collection.insert_one(user_data)
print(f"Inserted document with _id: {result.inserted_id}")