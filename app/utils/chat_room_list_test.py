import os
from pymongo import MongoClient
from datetime import datetime

# 환경변수에서 Mongo URI 가져오기
mongo_uri = os.getenv('MONGO_URI', 'mongodb://cornsoup:Chobob311^^@210.110.103.135:27017/itching_mongodb?authSource=admin')

# MongoDB 클라이언트 설정
client = MongoClient(mongo_uri)

# 데이터베이스와 컬렉션 선택
db = client['itching_mongodb']
collection = db['Chat_room_list_test']

# 추가할 데이터 정의 (freelancer_user_id를 모두 freelancer01로 설정)
new_chat_rooms = [
    {
      "chat_room_id": 1010,
      "participants_mapping": {
        "freelancer_user_id": "freelancer01",  # 수정됨
        "client_user_id": "client03"
      },
      "support_language_mapping": {
        "freelancer_language": "English",
        "client_language": "Korean"
      },
      "pin_status_mapping": {
        "freelancer01": True,
        "client03": False
      },
      "message_mapping": [
        {
          "sender_user_id": "freelancer01",  # 수정됨
          "message_content": "Hello!",
          "status": "read",
          "created_at": "2024-01-01T12:00:00Z"
        },
        {
          "sender_user_id": "client03",
          "message_content": "프로젝트에 관심 있으신가요?",
          "status": "read",
          "created_at": "2024-01-01T12:10:00Z"
        }
      ],
      "is_new_notification": False,
      "blocked_users": [],
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-02T14:00:00Z"
    },
    {
      "chat_room_id": 2020,
      "participants_mapping": {
        "freelancer_user_id": "freelancer01",  # 수정됨
        "client_user_id": "client04"
      },
      "support_language_mapping": {
        "freelancer_language": "Spanish",
        "client_language": "English"
      },
      "pin_status_mapping": {
        "freelancer01": False,
        "client04": True
      },
      "message_mapping": [
        {
          "sender_user_id": "freelancer01",  # 수정됨
          "message_content": "Hola! ¿Cómo estás?",
          "status": "unread",
          "created_at": "2024-01-02T15:00:00Z"
        },
        {
          "sender_user_id": "client04",
          "message_content": "I'm fine, thanks! Let's talk about the project.",
          "status": "read",
          "created_at": "2024-01-02T15:10:00Z"
        }
      ],
      "is_new_notification": True,
      "blocked_users": [],
      "created_at": "2024-01-02T15:00:00Z",
      "updated_at": "2024-01-02T16:00:00Z"
    },
    {
      "chat_room_id": 3030,
      "participants_mapping": {
        "freelancer_user_id": "freelancer01",  # 수정됨
        "client_user_id": "client05"
      },
      "support_language_mapping": {
        "freelancer_language": "French",
        "client_language": "Korean"
      },
      "pin_status_mapping": {
        "freelancer01": False,
        "client05": False
      },
      "message_mapping": [
        {
          "sender_user_id": "freelancer01",  # 수정됨
          "message_content": "Bonjour! Intéressé par votre projet.",
          "status": "unread",
          "created_at": "2024-01-03T09:00:00Z"
        },
        {
          "sender_user_id": "client05",
          "message_content": "Merci pour votre réponse, discutons-en!",
          "status": "read",
          "created_at": "2024-01-03T09:15:00Z"
        }
      ],
      "is_new_notification": True,
      "blocked_users": [],
      "created_at": "2024-01-03T09:00:00Z",
      "updated_at": "2024-01-03T09:20:00Z"
    }
]

# 데이터 삽입
result = collection.insert_many(new_chat_rooms)
print(f"Inserted documents with _ids: {result.inserted_ids}")


