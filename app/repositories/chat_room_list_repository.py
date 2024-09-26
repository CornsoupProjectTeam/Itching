#chat_room_list_repository.py
from typing import List
from app.models.mongodb_chat_room_management import ChatRoomManagement

class ChatRoomRepository:
    def __init__(self, db=None):
        self.db = db  # MongoDB 연결 객체가 필요한 경우 처리할 수 있습니다. 여기서는 mongoengine이 직접 관리.

    def get_chat_rooms_by_user_id(self, user_id: str) -> List[ChatRoomManagement]:
        """사용자가 참여한 모든 채팅방을 검색"""
        return list(ChatRoomManagement.objects(participants_mapping__freelancer_user_id=user_id))

    # ChatRoomRepository 수정
    def get_filtered_chat_rooms(self, chat_room_ids: List[str], user_id: str) -> List[ChatRoomManagement]:
        """채팅방 ID 목록에 해당하며, 차단되지 않고 삭제되지 않은 채팅방을 필터링"""
        return list(ChatRoomManagement.objects(
            chat_room_id__in=chat_room_ids,
            blocked_users__blocked_user_id__ne=user_id,  # 차단되지 않은 유저 필터링
            is_deleted=False
        ).order_by('-updated_at'))
