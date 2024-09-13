# mysql_chat_room_master.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ChatRoomMaster(db.Model):
    __tablename__ = 'chat_room_master'

    chat_room_id = db.Column(db.String(50), primary_key=True)
    quotation_id = db.Column(db.String(50), nullable=True)
    freelancer_user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=True)
    client_user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=True)
    start_post_id = db.Column(db.String(50), nullable=True)
    freelancer_trade_status = db.Column(db.Integer, nullable=False)
    client_trade_status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    freelancer = db.relationship('Login', foreign_keys=[freelancer_user_id], backref='freelancer_chatrooms')
    client = db.relationship('Login', foreign_keys=[client_user_id], backref='client_chatrooms')

    def __repr__(self):
        return f'<ChatRoomMaster {self.chat_room_id}>'
