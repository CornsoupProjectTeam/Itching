# chat_room_service.py
from app.domain.chat_room_domain import ChatRoom
from app.repositories.chat_room_repository import ChatRoomRepository

class ChatRoomService:
    def __init__(self):
        self.chat_room_repository = ChatRoomRepository()

    def send_message(self, chat_room_id, sender_id, receiver_id, message):
        """채팅 메시지 전송 (sender -> receiver)"""
        chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        chat_room.add_message(sender_id, receiver_id, message)
        self.chat_room_repository.save(chat_room)

    def get_received_messages(self, chat_room_id, user_id):
        """특정 사용자가 수신한 메시지 가져오기"""
        chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        return chat_room.get_messages_for_user(user_id)

