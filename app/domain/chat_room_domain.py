#app/domain/chat_room_domain.py
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

# ENUM 정의
class UserType(Enum):
    CLIENT = 'Client'
    FREELANCER = 'Freelancer'

class TradeStatus(Enum):
    IN_PROGRESS = 'In progress'
    COMPLETED = 'Completed'

class ChatRoom:
    def __init__(self, chat_room_id: str, user_id: str, user_type: UserType, 
                 start_post_id: Optional[str], is_deleted: bool, is_blocked: bool, 
                 is_new_notification: bool, trade_status: TradeStatus, pin_status: bool, 
                 support_language: Optional[str], created_at: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None, messages: Optional[List[Dict[str, str]]] = None):
        self.chat_room_id = chat_room_id                   # 채팅방 ID
        self.participants_mapping = {user_id: user_type}   # 사용자와 그 역할 (Client 또는 Freelancer)
        self.start_post_id = start_post_id                 # 게시물 ID (Optional)
        self.trade_status = trade_status                   # 거래 상태 (In progress, Completed)
        self.is_deleted = is_deleted                       # 삭제 여부
        self.is_blocked = is_blocked                       # 차단 여부
        self.is_new_notification = is_new_notification     # 새 알림 여부
        self.pin_status = pin_status                       # 채팅방 고정 여부
        self.support_language = support_language           # 지원 언어 (Optional)
        self.created_at = created_at or datetime.now()      # 생성일
        self.updated_at = updated_at or datetime.now()      # 수정일
        self.messages = messages or []                     # 메시지 목록

    def add_message(self, sender_id: str, receiver_id: str, message_content: str):
        """채팅 메시지를 추가하고 발신자와 수신자를 지정"""
        message = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message_content': message_content,
            'created_at': datetime.now()
        }
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_messages_for_user(self, user_id: str) -> List[Dict[str, str]]:
        """특정 사용자가 수신한 메시지만 반환"""
        return [msg for msg in self.messages if msg['receiver_id'] == user_id]

    def update_trade_status(self, new_status: TradeStatus):
        """거래 상태를 업데이트"""
        self.trade_status = new_status
        self.updated_at = datetime.now()

    def toggle_pin_status(self):
        """채팅방 고정 여부를 토글"""
        self.pin_status = not self.pin_status
        self.updated_at = datetime.now()

    def mark_as_deleted(self):
        """채팅방을 삭제된 상태로 마크"""
        self.is_deleted = True
        self.updated_at = datetime.now()

    def mark_as_blocked(self):
        """채팅방을 차단된 상태로 마크"""
        self.is_blocked = True
        self.updated_at = datetime.now()

    def mark_new_notification(self, has_new_notification: bool):
        """새 알림 여부 업데이트"""
        self.is_new_notification = has_new_notification
        self.updated_at = datetime.now()
