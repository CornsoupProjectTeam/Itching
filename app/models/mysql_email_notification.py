# mysql_email_notification.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EmailNotification(db.Model):
    __tablename__ = 'EMAIL_NOTIFICATION'

    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey('LOGIN.user_id'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('LOGIN', backref='email_notifications')

    def __repr__(self):
        return f"{self.email} - {self.message_type}"
