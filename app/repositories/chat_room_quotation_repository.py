# app/repositories/chat_room_quotation_repository.py

from app.models.mongodb_chat_room_quotation import ChatRoomQuotation

class ChatRoomQuotationRepository:
    @staticmethod
    def save(quotation):
        # 데이터 저장
        quotation.save()

    @staticmethod
    def find_by_chatroom_id(chatroom_id):
        # 채팅방 ID로 견적서 찾기
        return ChatRoomQuotation.objects(chatroom_id=chatroom_id).first()

    @staticmethod
    def update(quotation_id, updated_data):
        # 견적서 업데이트
        quotation = ChatRoomQuotation.objects(quotation_id=quotation_id).first()
        if quotation:
            quotation.update(**updated_data)
            return quotation
        return None
