from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ChatRoomScanner(db.Model):
    __tablename__ = 'CHAT_ROOM_SCANNER'
    
    chat_room_scanner_id = db.Column(db.String(50), primary_key=True)
    quotation_id = db.Column(db.String(50), db.ForeignKey('CHAT_ROOM_QUOTATION.quotation_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    quotation = db.relationship('ChatRoomQuotation', backref=db.backref('scanners', uselist=False))
