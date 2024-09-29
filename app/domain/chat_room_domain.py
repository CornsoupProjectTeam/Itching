#chat_room_domain.py
from datetime import datetime
from typing import List, Dict, Optional

class ChatRoom:
    def __init__(self, chat_room_id: str, user_id: str, user_type: str, quotation_id: str, 
                 start_post_id: str, trade_status: str, is_deleted: bool, is_blocked: bool, 
                 is_new_notification: bool, pin_status: bool, support_language: str, 
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, 
                 messages: Optional[List[Dict[str, str]]] = None):
        self.chat_room_id = chat_room_id                   # 채팅방 ID
        self.participants_mapping = {user_id: user_type}   # 사용자와 그 역할 (Client 또는 Freelancer)
        self.quotation_id = quotation_id                   # 견적서 ID
        self.start_post_id = start_post_id                 # 게시물 ID
        self.trade_status = trade_status                   # 거래 상태 (In progress, Completed)
        self.is_deleted = is_deleted                       # 삭제 여부
        self.is_blocked = is_blocked                       # 차단 여부
        self.is_new_notification = is_new_notification     # 새 알림 여부
        self.pin_status = pin_status                       # 채팅방 고정 여부
        self.support_language = support_language           # 지원 언어
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

    # def has_participant(self, user_id: str) -> bool:
    #     """사용자가 채팅방에 참여하고 있는지 확인"""
    #     return user_id in self.participants_mapping

    def is_user_blocked(self) -> bool:
        """채팅방에서 사용자가 차단되었는지 확인"""
        return self.is_blocked

    def is_chat_room_deleted(self) -> bool:
        """채팅방이 삭제되었는지 확인"""
        return self.is_deleted

    def get_most_recent_message(self) -> Optional[Dict[str, str]]:
        """채팅방에서 가장 최근 메시지를 가져오기"""
        if self.messages:
            return self.messages[-1]
        return None

    def pin_chat_room(self):
        """채팅방을 상단에 고정"""
        self.pin_status = True
        self.updated_at = datetime.now()

    def unpin_chat_room(self):
        """채팅방을 상단에서 해제"""
        self.pin_status = False
        self.updated_at = datetime.now()

    def update_trade_status(self, new_status: str):
        """거래 상태를 업데이트"""
        if new_status in ['In progress', 'Completed']:
            self.trade_status = new_status
            self.updated_at = datetime.now()

    def update_support_language(self, new_language: str):
        """지원 언어를 업데이트"""
        self.support_language = new_language
        self.updated_at = datetime.now()

    def block_user(self):
        """사용자를 차단"""
        self.is_blocked = True
        self.updated_at = datetime.now()

    def unblock_user(self):
        """사용자 차단을 해제"""
        self.is_blocked = False
        self.updated_at = datetime.now()
