# chat_room_list_service.py
from typing import List, Dict
from pymongo import MongoClient

class ChatRoomService:
    def __init__(self, mongo_uri: str):
        # MongoDB 클라이언트 설정
        self.client = MongoClient(mongo_uri)
        self.db = self.client['itching_mongodb']
        self.collection = self.db['Chat_room_list_test']

    def get_chat_rooms_for_user(self, freelancer_user_id: str) -> List[Dict]:
        """freelancer01이 참여한 채팅방 목록을 가져옴"""
        chat_rooms = list(self.collection.find({
            'participants_mapping.freelancer_user_id': freelancer_user_id
        }))
        return chat_rooms

    def get_chat_room_by_id(self, chat_room_id: str) -> Dict:
        """chat_room_id에 해당하는 채팅방 정보를 가져옴"""
        chat_room = self.collection.find_one({'chat_room_id': int(chat_room_id)})
        return chat_room
