from app import db
from datetime import datetime

class ChatRoomMaster(db.Model):
    __tablename__ = 'CHAT_ROOM_MASTER'
    
    chat_room_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id'), nullable=False)
    user_type = db.Column(db.Enum('Client', 'Freelancer'), nullable=False)
    start_post_id = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    is_new_notification = db.Column(db.Boolean, default=False)
    trade_st = db.Column(db.Enum('In progress', 'Completed'))
    pin_st = db.Column(db.Boolean, default=False)
    support_language = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('chat_room_masters', lazy=True))
