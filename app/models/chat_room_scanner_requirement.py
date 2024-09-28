from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ChatRoomScannerRequirement(db.Model):
    __tablename__ = 'CHAT_ROOM_SCANNER_REQUIREMENT'
    
    requirement_id = db.Column(db.String(50), primary_key=True)
    chat_room_scanner_id = db.Column(db.String(50), db.ForeignKey('CHAT_ROOM_SCANNER.chat_room_scanner_id', ondelete='CASCADE'))
    sequence = db.Column(db.Integer)
    requirement = db.Column(db.Text)
    score = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    chat_room_scanner = db.relationship('ChatRoomScanner', backref=db.backref('requirements', lazy=True, cascade="all, delete-orphan"))
