from typing import List, Optional, Dict
from app.repositories.chat_room_list_repository import ChatRoomRepository
from app.models.mongodb_chat_room_management import ChatRoomManagement

class ChatRoomService:
    def __init__(self, chat_room_repository: ChatRoomRepository):
        self.chat_room_repository = chat_room_repository

    def get_all_chat_rooms_for_user(self, user_id: str) -> List[ChatRoomManagement]:
        #사용자가 참여한 모든 채팅방을 가져오기
        return self.chat_room_repository.get_chat_rooms_by_user_id(user_id)

    def get_filtered_and_sorted_chat_rooms_for_user(self, user_id: str) -> List[ChatRoomManagement]:
        #사용자가 참여한 채팅방을 필터링하고 최신 수정일 순으로 정렬
        chat_rooms = self.get_all_chat_rooms_for_user(user_id)
        chat_room_ids = [chat_room.chat_room_id for chat_room in chat_rooms]
        return self.chat_room_repository.get_filtered_chat_rooms(chat_room_ids, user_id)

    def get_last_message_info_from_chat_room(self, chat_room: ChatRoomManagement) -> Optional[Dict[str, str]]:
        #채팅방에서 가장 최근의 메시지 정보 가져오기
        if chat_room.message_mapping:
            last_message = chat_room.message_mapping[-1]
            return {
                "sender_id": last_message.sender_user_id,
                "message": last_message.message_content
            }
        return None
