# #chat_room_service.py
# from typing import List, Dict
# from pymongo import MongoClient
# from app.domain.chat_room_domain import ChatRoom
# from app.repositories.chat_room_repository import ChatRoomRepository

# class ChatRoomService:
#     def __init__(self, mongo_uri: str, db_session):
#         self.client = MongoClient(mongo_uri)
#         self.db = self.client['itching_mongodb']
#         self.collection = self.db['Chat_room_list_test']
#         self.chat_room_repository = ChatRoomRepository(db_session)

#     def get_chat_rooms_for_user(self, freelancer_user_id: str) -> List[Dict]:
#         chat_rooms = list(self.collection.find({
#             'participants_mapping.freelancer_user_id': freelancer_user_id
#         }))
#         return chat_rooms

#     def get_chat_room_data(self, freelancer_user_id: str) -> List[Dict]:
#         chat_rooms = self.get_chat_rooms_for_user(freelancer_user_id)
        
#         chat_room_data = []
#         for chat_room in chat_rooms:
#             last_message_info = chat_room.get("message_mapping", [])[-1] if chat_room.get("message_mapping") else None
#             chat_room_data.append({
#                 "chat_room_id": chat_room["chat_room_id"],
#                 "client_user_id": chat_room["participants_mapping"]["client_user_id"],
#                 "last_message": last_message_info["message_content"] if last_message_info else "No messages",
#                 "sender_id": last_message_info["sender_user_id"] if last_message_info else "Unknown",
#                 "updated_at": chat_room["updated_at"]
#             })

#         return chat_room_data

#     def get_chat_room_by_id(self, chat_room_id: str) -> Dict:
#         chat_room = self.collection.find_one({'chat_room_id': int(chat_room_id)})
#         return chat_room

#     def send_message(self, chat_room_id, sender_id, receiver_id, message):
#         chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        
#         if chat_room:
#             chat_room.add_message(sender_id, receiver_id, message)
#             self.chat_room_repository.save(chat_room)

#             self.chat_room_repository.add_message(chat_room_id, sender_id, receiver_id, message)

#     def get_received_messages(self, chat_room_id, user_id):
#         chat_room = self.chat_room_repository.find_by_id(chat_room_id)
#         if chat_room:
#             return chat_room.get_messages_for_user(user_id)
#         return []

#     def get_most_recent_message(self, chat_room_id: str, user_id: str) -> Dict:
#         return self.chat_room_repository.get_most_recent_message(chat_room_id, user_id)

from typing import List, Dict
from app.domain.chat_room_domain import ChatRoom
from app.repositories.chat_room_repository import ChatRoomRepository

class ChatRoomService:
    def __init__(self, db_session):
        self.chat_room_repository = ChatRoomRepository(db_session)

    def get_chat_rooms_for_user(self, freelancer_user_id: str) -> List[Dict]:
        # MySQL에서 채팅방 데이터 가져오기
        chat_rooms = self.chat_room_repository.get_chat_rooms_by_user_id(freelancer_user_id)
        return chat_rooms

    def get_chat_room_data(self, freelancer_user_id: str) -> List[Dict]:
        chat_rooms = self.get_chat_rooms_for_user(freelancer_user_id)
        
        chat_room_data = []
        for chat_room in chat_rooms:
            last_message_info = chat_room.get("last_message_info", None)
            chat_room_data.append({
                "chat_room_id": chat_room["chat_room_id"],
                "client_user_id": chat_room["client_user_id"],
                "last_message": last_message_info["message_content"] if last_message_info else "No messages",
                "sender_id": last_message_info["sender_user_id"] if last_message_info else "Unknown",
                "updated_at": chat_room["updated_at"]
            })

        return chat_room_data

    def get_chat_room_by_id(self, chat_room_id: str) -> Dict:
        # MySQL에서 채팅방 정보 가져오기
        chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        return chat_room

    def send_message(self, chat_room_id: str, sender_id: str, receiver_id: str, message: str):
        chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        
        if chat_room:
            chat_room.add_message(sender_id, receiver_id, message)
            self.chat_room_repository.save(chat_room)

            # 메시지 저장 로직 추가
            self.chat_room_repository.add_message(chat_room_id, sender_id, receiver_id, message)

    def get_received_messages(self, chat_room_id: str, user_id: str) -> List[Dict]:
        chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        if chat_room:
            return chat_room.get_messages_for_user(user_id)
        return []

    def get_most_recent_message(self, chat_room_id: str, user_id: str) -> Dict:
        return self.chat_room_repository.get_most_recent_message(chat_room_id, user_id)


