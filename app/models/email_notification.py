from app import db
from datetime import datetime

class EmailNotification(db.Model):
    __tablename__ = 'EMAIL_NOTIFICATION'
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('email_notifications', lazy=True, cascade="all, delete-orphan"))
