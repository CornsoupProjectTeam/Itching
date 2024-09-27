from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'PAYMENT'
    
    chat_room_id = db.Column(db.String(50), db.ForeignKey('CHAT_ROOM_MASTER.chat_room_id'), primary_key=True)
    quotation_id = db.Column(db.String(50), db.ForeignKey('CHAT_ROOM_QUOTATION.quotation_id'), nullable=False)
    freelancer_user_id = db.Column(db.String(50), db.ForeignKey('USER_INFORMATION.user_id'), nullable=False)
    client_user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id'), nullable=False)
    user_name = db.Column(db.String(100))
    price_unit = db.Column(db.Enum('KRW', 'USD'), default='KRW')
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_st = db.Column(db.Enum('Pending', 'Success', 'Fail'), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    chat_room_master = db.relationship('ChatRoomMaster', backref=db.backref('payments', uselist=False))
    quotation = db.relationship('ChatRoomQuotation', backref=db.backref('payments', uselist=False))
    freelancer_user = db.relationship('UserInformation', foreign_keys=[freelancer_user_id], backref=db.backref('freelancer_payments', lazy=True))
    client_user = db.relationship('UserInformation', foreign_keys=[client_user_id], backref=db.backref('client_payments', lazy=True))
