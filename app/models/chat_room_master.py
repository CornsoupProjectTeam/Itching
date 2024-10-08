#app/models/chat_room_master.py
import uuid
from app import db
from datetime import datetime

class ChatRoomMaster(db.Model):
    __tablename__ = 'CHAT_ROOM_MASTER'
    
    chat_room_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID 자동 생성
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id'), nullable=False)
    other_user_id = db.Column(db.String(20), nullable=False)  # other_user_id 필드 추가
    user_type = db.Column(db.Enum('Client', 'Freelancer'), nullable=False)
    start_post_id = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    is_new_notification = db.Column(db.Boolean, default=False)
    trade_st = db.Column(db.Enum('In progress', 'Completed', 'Canceled'), default='In progress')
    pin_st = db.Column(db.Boolean, default=False)
    support_language = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('chat_room_masters', lazy=True))
    
      # to_dict 메서드 추가
    def to_dict(self):
        return {
            "chat_room_id": self.chat_room_id,
            "user_id": self.user_id,
            "other_user_id": self.other_user_id,
            "user_type": self.user_type,
            "start_post_id": self.start_post_id,
            "is_deleted": self.is_deleted,
            "is_blocked": self.is_blocked,
            "is_new_notification": self.is_new_notification,
            "trade_st": self.trade_st,
            "pin_st": self.pin_st,
            "support_language": self.support_language,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }