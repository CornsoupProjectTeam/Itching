# mongodb_chat_room_management.py

from mongoengine import Document, StringField, BooleanField, DateTimeField, DictField, ListField, EmbeddedDocument, EmbeddedDocumentField
import datetime

# 메시지의 Embedded Document 정의
class Message(EmbeddedDocument):
    sender_user_id = StringField(max_length=20, required=True)  # 발신 유저 ID
    message_content = StringField(required=True)  # 메시지 내용
    status = StringField(choices=["unread", "read"], default="unread")  # 메시지 상태 (읽음, 읽지 않음)
    created_at = DateTimeField(default=datetime.datetime.utcnow)  # 메시지 생성일

# 차단된 유저의 Embedded Document 정의
class BlockedUser(EmbeddedDocument):
    blocker_user_id = StringField(max_length=20, required=True)  # 차단한 유저 ID
    blocked_user_id = StringField(max_length=20, required=True)  # 차단된 유저 ID
    blocked_at = DateTimeField(default=datetime.datetime.utcnow)  # 차단 일시

# 채팅방 관리 Document 정의
class ChatRoomManagement(Document):
    chat_room_id = StringField(max_length=50, required=True, unique=True)  # 채팅방 ID
    participants_mapping = DictField(required=True)  # 참여 유저 맵핑 (freelancer_user_id, client_user_id)
    support_language_mapping = DictField(required=True)  # 언어 지원 맵핑 (freelancer_language, client_language)
    pin_status_mapping = DictField(default={})  # 상단 고정 여부 맵핑
    message_mapping = ListField(EmbeddedDocumentField(Message))  # 메시지 리스트
    is_new_notification = BooleanField(default=False)  # 새로운 알림 표시 여부
    blocked_users = ListField(EmbeddedDocumentField(BlockedUser))  # 차단 유저 리스트
    is_deleted = BooleanField(default=False)  # 논리적 삭제 여부
    created_at = DateTimeField(default=datetime.datetime.utcnow)  # 생성일
    updated_at = DateTimeField(default=datetime.datetime.utcnow)  # 수정일

    # 새로운 메시지 추가 시 알림 상태 변경 로직
    def add_message(self, sender_user_id, message_content):
        message = Message(sender_user_id=sender_user_id, message_content=message_content, status="unread")
        self.message_mapping.append(message)
        self.is_new_notification = True  # 읽지 않은 메시지가 생기면 알림 상태를 True로 변경
        self.updated_at = datetime.datetime.utcnow()  # 수정 시간 업데이트
        self.save()

    # 메시지 읽음 처리 시 알림 상태 변경
    def mark_messages_as_read(self, user_id):
        for message in self.message_mapping:
            if message.sender_user_id != user_id and message.status == "unread":
                message.status = "read"
        self.is_new_notification = False  # 모든 메시지가 읽히면 알림 상태를 False로 변경
        self.updated_at = datetime.datetime.utcnow()  # 수정 시간 업데이트
        self.save()

    # 논리적 삭제 처리
    def delete_chat_room(self):
        self.is_deleted = True  # 논리적 삭제 플래그를 True로 설정
        self.updated_at = datetime.datetime.utcnow()  # 수정 시간 업데이트
        self.save()

    def __str__(self):
        return self.chat_room_id