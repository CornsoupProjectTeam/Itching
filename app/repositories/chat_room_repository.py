#chat_room_repository.py
from app.models.mongodb_chat_room_management import ChatRoomManagement  # 이름을 ChatRoomManagement로 수정

class ChatRoomRepository:
    def find_by_id(self, chat_room_id):
        # MongoDB에서 ChatRoom 조회
        return ChatRoomManagement.objects(chat_room_id=chat_room_id).first()  # ChatRoomManagement 사용

    def save(self, chat_room):
        # MongoDB에 ChatRoom 저장
        chat_room_model = ChatRoomManagement(  # ChatRoomManagement 사용
            chat_room_id=chat_room.chat_room_id,
            quotation_id=chat_room.quotation_id,
            freelancer_user_id=chat_room.freelancer_user_id,
            client_user_id=chat_room.client_user_id,
            start_post_id=chat_room.start_post_id,
            freelancer_trade_status=chat_room.freelancer_trade_status,
            client_trade_status=chat_room.client_trade_status,
            created_at=chat_room.created_at,
            updated_at=chat_room.updated_at,
            message_mapping=chat_room.messages  # 메시지 추가
        )
        chat_room_model.save()
