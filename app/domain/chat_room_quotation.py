# app/domain/chat_room_quotation.py

from datetime import datetime
from app.models.mongodb_chat_room_quotation import ChatRoomQuotation

class ChatRoomQuotationDomain:
    def __init__(self, quotation_id, chatroom_id, participants, quotation_status, 
                 requirements_mapping, quotation, number_of_drafts, notification_dates, 
                 revision_count, additional_revision_purchase_available, 
                 commercial_use_allowed, high_resolution_file_available, delivery_route):
        self.quotation_id = quotation_id  # 추가된 필드
        self.chatroom_id = chatroom_id
        self.participants = participants
        self.quotation_status = quotation_status
        self.requirements_mapping = requirements_mapping
        self.quotation = quotation
        self.number_of_drafts = number_of_drafts
        self.notification_dates = notification_dates
        self.revision_count = revision_count
        self.additional_revision_purchase_available = additional_revision_purchase_available
        self.commercial_use_allowed = commercial_use_allowed
        self.high_resolution_file_available = high_resolution_file_available
        self.delivery_route = delivery_route
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_quotation(self, updated_fields):
        # 필요한 필드들을 업데이트
        for key, value in updated_fields.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def to_entity(self):
        # ChatRoomQuotation MongoDB 엔티티 생성 및 반환
        return ChatRoomQuotation(
            quotation_id=self.quotation_id,  # 추가된 필드
            chatroom_id=self.chatroom_id,
            participants=self.participants,
            quotation_status=self.quotation_status,
            requirements_mapping=self.requirements_mapping,
            quotation=self.quotation,
            number_of_drafts=self.number_of_drafts,
            notification_dates=self.notification_dates,
            revision_count=self.revision_count,
            additional_revision_purchase_available=self.additional_revision_purchase_available,
            commercial_use_allowed=self.commercial_use_allowed,
            high_resolution_file_available=self.high_resolution_file_available,
            delivery_route=self.delivery_route,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
