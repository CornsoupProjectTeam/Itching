# app/services/chat_room_quotation_service.py

from app.domain.chat_room_quotation import ChatRoomQuotationDomain
from app.repositories.chat_room_quotation_repository import ChatRoomQuotationRepository

class ChatRoomQuotationService:
    @staticmethod
    def create_quotation(data):
        # ChatRoomQuotation 도메인 객체 생성
        quotation_domain = ChatRoomQuotationDomain(**data)
        # 도메인 객체를 Entity로 변환하여 저장
        ChatRoomQuotationRepository.save(quotation_domain.to_entity())
        return quotation_domain

    @staticmethod
    def get_quotation(chatroom_id):
        return ChatRoomQuotationRepository.find_by_chatroom_id(chatroom_id)

    @staticmethod
    def update_quotation(quotation_id, updated_data):
        return ChatRoomQuotationRepository.update(quotation_id, updated_data)
