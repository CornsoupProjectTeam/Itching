#.mongodb_message_mapping.py
import mongoengine as me
from datetime import datetime

class MessageMapping(me.Document):
    """
    MongoDB에서 메시지 정보를 관리하는 MessageMapping 모델.
    """
    message_mapping_id = me.StringField(primary_key=True)
    sender_user_id = me.StringField(required=True)
    receiver_user_id = me.StringField(required=True)
    message_content = me.StringField(required=True)
    status = me.StringField(default="sent")  # 메시지 상태: 'sent', 'received', 'read' 등
    created_at = me.DateTimeField(default=datetime.now)
    updated_at = me.DateTimeField(default=datetime.now)

    meta = {
        'collection': 'message_mappings',  # MongoDB 컬렉션 이름
        'indexes': [
            'sender_user_id',
            'receiver_user_id',
            '-created_at',  # 내림차순으로 인덱스 생성 (최신 메시지를 빠르게 조회 가능)
        ]
    }
