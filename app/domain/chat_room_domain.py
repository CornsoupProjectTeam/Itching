# app/domain/chat_room_domain.py
from datetime import datetime
from enum import Enum

class UserType(Enum):
    CLIENT = 'Client'
    FREELANCER = 'Freelancer'

class TradeStatus(Enum):
    IN_PROGRESS = 'In progress'
    COMPLETED = 'Completed'

class ChatRoom:
    def __init__(self, chat_room_id, user_id, other_user_id, user_type, start_post_id, is_deleted, is_blocked,
                 is_new_notification, trade_status, pin_status, support_language, created_at=None, updated_at=None):
        self.chat_room_id = chat_room_id
        self.user_id = user_id
        self.other_user_id = other_user_id
        self.user_type = UserType(user_type)
        self.start_post_id = start_post_id
        self.is_deleted = bool(is_deleted)
        self.is_blocked = bool(is_blocked)
        self.is_new_notification = bool(is_new_notification)
        self.trade_status = TradeStatus(trade_status)
        self.pin_status = bool(pin_status)
        self.support_language = support_language
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        
    def to_dict(self):
        """
        객체를 JSON 직렬화 가능한 딕셔너리로 변환
        """
        return {
            'chat_room_id': self.chat_room_id,
            'user_id': self.user_id,
            'other_user_id' : self.other_user_id,
            'user_type': self.user_type.value,  # Enum을 문자열로 변환
            'start_post_id': self.start_post_id,
            'is_deleted': self.is_deleted,
            'is_blocked': self.is_blocked,
            'is_new_notification': self.is_new_notification,
            'trade_status': self.trade_status.value,  # Enum을 문자열로 변환
            'pin_status': self.pin_status,
            'support_language': self.support_language,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Message:
    def __init__(self, message_mapping_id, sender_user_id, receiver_user_id, message_content, status, created_at=None, updated_at=None):
        self.message_mapping_id = message_mapping_id
        self.sender_user_id = sender_user_id
        self.receiver_user_id = receiver_user_id
        self.message_content = message_content
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
