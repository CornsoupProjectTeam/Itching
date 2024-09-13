# mysql_payment.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'PAYMENT'

    chat_room_id = db.Column(db.String(50), db.ForeignKey('chat_room_master.chat_room_id'), primary_key=True)
    quotation_id = db.Column(db.String(50), nullable=False)
    freelancer_user_id = db.Column(db.String(20), db.ForeignKey('LOGIN.user_id'), nullable=False)
    client_user_id = db.Column(db.String(20), db.ForeignKey('LOGIN.user_id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=True)
    project_title = db.Column(db.String(200), nullable=True)
    price_unit = db.Column(db.String(5), nullable=True)
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_st = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    freelancer = db.relationship('LOGIN', foreign_keys=[freelancer_user_id], backref='freelancer_payments')
    client = db.relationship('LOGIN', foreign_keys=[client_user_id], backref='client_payments')
    chat_room = db.relationship('ChatRoomMaster', backref='payment')

    def __repr__(self):
        return self.chat_room_id
