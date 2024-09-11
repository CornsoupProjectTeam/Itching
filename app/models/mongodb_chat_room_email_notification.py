# mongodb_chat_room_email_notification.py

from mongoengine import Document, StringField, DateTimeField, DictField, EmbeddedDocument, EmbeddedDocumentField, ListField, IntField
import datetime

# 알림 정보에 대한 Embedded Document 정의
class Notification(EmbeddedDocument):
    sequence = IntField(required=True)  # 알림 시퀀스 번호
    receiver_user_id = StringField(max_length=20, required=True)  # 수신 유저 ID
    sender_user_id = StringField(max_length=20, required=True)  # 발신 유저 ID
    message = StringField(required=True)  # 알림 메시지
    created_at = DateTimeField(default=datetime.datetime.utcnow)  # 알림 생성일

# 메인 ChatRoomEmailNotification Document 정의
class ChatRoomEmailNotification(Document):
    chat_room_id = IntField(max_length=50, required=True, unique=True)  # 채팅방 ID
    user_id_email_mapping = DictField(required=True)  # 사용자 ID와 이메일의 맵핑
    notification_mapping = ListField(EmbeddedDocumentField(Notification))  # 알림 매핑
    created_at = DateTimeField(default=datetime.datetime.utcnow)  # 생성일

    def __str__(self):
        return f"ChatRoomEmailNotification: {self.chat_room_id}:{self.receiver_user_id}"