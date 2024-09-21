from datetime import datetime
from typing import List, Dict, Optional

class ChatRoomList:
    def __init__(
        self, 
        chat_room_id: str, 
        participants_mapping: Dict[str, str],
        support_language_mapping: List[str],
        pin_status_mapping: Dict[str, bool],
        message_mapping: List[Dict[str, str]],
        is_new_notification: bool,
        blocked_users: List[str],
        is_deleted: bool,
        created_at: datetime,
        updated_at: datetime
    ):
        self.chat_room_id = chat_room_id
        self.participants_mapping = participants_mapping
        self.support_language_mapping = support_language_mapping
        self.pin_status_mapping = pin_status_mapping
        self.message_mapping = message_mapping
        self.is_new_notification = is_new_notification
        self.blocked_users = blocked_users
        self.is_deleted = is_deleted
        self.created_at = created_at
        self.updated_at = updated_at

    def has_participant(self, user_id: str) -> bool:
        """사용자가 채팅방에 참여하고 있는지 확인"""
        return user_id in self.participants_mapping

    def is_user_blocked(self, user_id: str) -> bool:
        """해당 사용자가 채팅방에서 차단되었는지 확인"""
        return user_id in self.blocked_users

    def is_chat_room_deleted(self) -> bool:
        """채팅방이 삭제되었는지 확인"""
        return self.is_deleted

    def get_most_recent_message(self) -> Optional[Dict[str, str]]:
        """채팅방에서 가장 최근 메시지를 가져오기"""
        if self.message_mapping:
            return self.message_mapping[-1]
        return None
