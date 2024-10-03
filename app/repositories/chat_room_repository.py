# #chat_room_repository.py
# from sqlalchemy.orm import Session
# from typing import List
# from app.models.chat_room_master import ChatRoomMaster
# from app.models.mongodb_message_mapping import MessageMapping  # MongoDB MessageMapping 모델
# from datetime import datetime
# import uuid  # UUID 생성용
# import mongoengine as me  # mongoengine을 me로 임포트
# from app.domain.chat_room_domain import ChatRoom, UserType, TradeStatus

# class ChatRoomRepository:
#     def __init__(self, db_session: Session):
#         self.db_session = db_session

#     def get_chat_rooms_by_user_id(self, user_id: str) -> List[ChatRoomMaster]:
#         """
#         주어진 사용자가 참여하고 있는 모든 채팅방을 검색
#         """
#         return self.db_session.query(ChatRoomMaster).filter_by(user_id=user_id).all()

#     def get_filtered_chat_rooms(self, chat_room_ids: List[str], user_id: str) -> List[ChatRoomMaster]:
#         """
#         주어진 채팅방 ID 목록에서, 해당 사용자가 차단되지 않았고 삭제되지 않은 채팅방을 필터링
#         """
#         return self.db_session.query(ChatRoomMaster).filter(
#             ChatRoomMaster.chat_room_id.in_(chat_room_ids),
#             ChatRoomMaster.is_blocked.is_(False),
#             ChatRoomMaster.is_deleted.is_(False)
#         ).all()

#     def find_by_id(self, chat_room_id: str) -> ChatRoomMaster:
#         """
#         채팅방 ID로 특정 채팅방을 조회
#         """
#         return self.db_session.query(ChatRoomMaster).filter_by(chat_room_id=chat_room_id).first()

#     def save(self, chat_room: ChatRoomMaster):
#         """
#         채팅방 객체를 SQL DB에 저장
#         """
#         if not chat_room.created_at:
#             chat_room.created_at = datetime.now()
#         chat_room.updated_at = datetime.now()

#         self.db_session.add(chat_room)
#         self.db_session.commit()

#     ### MongoDB 메시지 저장 및 조회 기능 ###

#     def add_message(self, chat_room_id: str, sender_id: str, receiver_id: str, message_content: str):
#         """
#         특정 채팅방에 메시지 추가 (MongoDB의 message_mappings 컬렉션에 저장)
#         """
#         message = MessageMapping(
#             message_mapping_id=str(uuid.uuid4()),  # UUID를 사용하여 고유 ID 생성
#             sender_user_id=sender_id,
#             receiver_user_id=receiver_id,
#             message_content=message_content,
#             status='sent',
#             created_at=datetime.now(),
#             updated_at=datetime.now()
#         )
#         message.save()  # MongoDB에 메시지 저장

#     def get_most_recent_message(self, chat_room_id: str, user_id: str):
#         """
#         특정 채팅방에서 가장 최근 메시지 가져오기 (MongoDB의 message_mappings에서 조회)
#         """
#         return MessageMapping.objects(
#             me.Q(sender_user_id=user_id) | me.Q(receiver_user_id=user_id)
#         ).order_by('-created_at').first()

#     def get_chat_room_messages(self, chat_room_id: str, limit: int = 20):
#         """
#         특정 채팅방의 메시지를 페이징 처리하여 가져오기 (MongoDB에서 조회)
#         """
#         return MessageMapping.objects(
#             me.Q(chat_room_id=chat_room_id)
#         ).order_by('-created_at').limit(limit)

#     def update_message_status(self, message_mapping_id: str, new_status: str):
#         """
#         메시지 상태 업데이트 (예: 'received', 'read')
#         """
#         message = MessageMapping.objects(message_mapping_id=message_mapping_id).first()
#         if message:
#             message.status = new_status
#             message.updated_at = datetime.now()
#             message.save()

#     ### 차단 및 차단 해제 기능 ###

#     def block_user(self, chat_room_id: str, user_id: str):
#         """
#         특정 채팅방에서 사용자를 차단
#         """
#         chat_room = self.find_by_id(chat_room_id)
#         if chat_room:
#             chat_room.is_blocked = True
#             chat_room.updated_at = datetime.now()
#             self.save(chat_room)

#     def unblock_user(self, chat_room_id: str, user_id: str):
#         """
#         특정 채팅방에서 사용자 차단 해제
#         """
#         chat_room = self.find_by_id(chat_room_id)
#         if chat_room:
#             chat_room.is_blocked = False
#             chat_room.updated_at = datetime.now()
#             self.save(chat_room)

#chat_room_repository.py
from sqlalchemy.orm import Session
from typing import List
from app.models.chat_room_master import ChatRoomMaster
from app.models.mongodb_message_mapping import MessageMapping  # MongoDB 메시지 모델
from datetime import datetime
import uuid  # UUID 생성용
import mongoengine as me  # mongoengine을 사용하여 MongoDB와 연결
from app.domain.chat_room_domain import ChatRoom

class ChatRoomRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_chat_rooms_by_user_id(self, user_id: str) -> List[ChatRoomMaster]:
        """
        주어진 사용자가 참여하고 있는 모든 채팅방을 검색
        """
        return self.db_session.query(ChatRoomMaster).filter_by(user_id=user_id).all()

    def get_filtered_chat_rooms(self, chat_room_ids: List[str], user_id: str) -> List[ChatRoomMaster]:
        """
        주어진 채팅방 ID 목록에서, 해당 사용자가 차단되지 않았고 삭제되지 않은 채팅방을 필터링
        """
        return self.db_session.query(ChatRoomMaster).filter(
            ChatRoomMaster.chat_room_id.in_(chat_room_ids),
            ChatRoomMaster.is_blocked.is_(False),
            ChatRoomMaster.is_deleted.is_(False)
        ).all()

    def find_by_id(self, chat_room_id: str) -> ChatRoomMaster:
        """
        채팅방 ID로 특정 채팅방을 조회
        """
        return self.db_session.query(ChatRoomMaster).filter_by(chat_room_id=chat_room_id).first()

    def save(self, chat_room: ChatRoomMaster):
        """
        채팅방 객체를 SQL DB에 저장
        """
        if not chat_room.created_at:
            chat_room.created_at = datetime.now()
        chat_room.updated_at = datetime.now()

        self.db_session.add(chat_room)
        self.db_session.commit()

    ### 메시지 저장 및 조회 기능 (MongoDB 사용) ###

    def add_message(self, chat_room_id: str, sender_id: str, receiver_id: str, message_content: str):
        """
        특정 채팅방에 메시지 추가 (MongoDB의 message_mappings 컬렉션에 저장)
        """
        message = MessageMapping(
            message_mapping_id=str(uuid.uuid4()),  # UUID를 사용하여 고유 ID 생성
            chat_room_id=chat_room_id,
            sender_user_id=sender_id,
            receiver_user_id=receiver_id,
            message_content=message_content,
            status='sent',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        message.save()  # MongoDB에 메시지 저장

    def get_most_recent_message(self, chat_room_id: str, user_id: str):
        """
        특정 채팅방에서 가장 최근 메시지 가져오기 (MongoDB의 message_mappings에서 조회)
        """
        return MessageMapping.objects(
            (me.Q(sender_user_id=user_id) | me.Q(receiver_user_id=user_id)) &
            (me.Q(chat_room_id=chat_room_id))
        ).order_by('-created_at').first()

    def get_chat_room_messages(self, chat_room_id: str, limit: int = 20):
        """
        특정 채팅방의 메시지를 페이징 처리하여 가져오기 (MongoDB에서 조회)
        """
        return MessageMapping.objects(
            chat_room_id=chat_room_id
        ).order_by('-created_at').limit(limit)

    def update_message_status(self, message_mapping_id: str, new_status: str):
        """
        메시지 상태 업데이트 (예: 'received', 'read')
        """
        message = MessageMapping.objects(message_mapping_id=message_mapping_id).first()
        if message:
            message.status = new_status
            message.updated_at = datetime.now()
            message.save()

    ### 차단 및 차단 해제 기능 ###

    def block_user(self, chat_room_id: str, user_id: str):
        """
        특정 채팅방에서 사용자를 차단
        """
        chat_room = self.find_by_id(chat_room_id)
        if chat_room:
            chat_room.is_blocked = True
            chat_room.updated_at = datetime.now()
            self.save(chat_room)

    def unblock_user(self, chat_room_id: str, user_id: str):
        """
        특정 채팅방에서 사용자 차단 해제
        """
        chat_room = self.find_by_id(chat_room_id)
        if chat_room:
            chat_room.is_blocked = False
            chat_room.updated_at = datetime.now()
            self.save(chat_room)

