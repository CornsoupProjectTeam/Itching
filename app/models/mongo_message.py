#. app/models/mongo_message.py
from pymongo import MongoClient
from datetime import datetime

class MongoMessage:
    def __init__(self, mongo_uri, db_name, collection_name="Message"):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_message(self, sender_user_id: str, receiver_user_id: str, message_content: str, status="sent"):
        message_data = {
            "sender_user_id": sender_user_id,
            "receiver_user_id": receiver_user_id,
            "message_content": message_content,
            "status": status,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = self.collection.insert_one(message_data)
        return str(result.inserted_id)

    def get_messages(self, chat_room_id: str, user_id: str):
        # 특정 채팅방의 메시지를 조회 (sender 또는 receiver가 해당 유저여야 함)
        messages = self.collection.find({
            "chat_room_id": chat_room_id,
            "$or": [
                {"sender_user_id": user_id},
                {"receiver_user_id": user_id}
            ]
        }).sort("created_at", 1)

        return [{**message, "_id": str(message["_id"])} for message in messages]
