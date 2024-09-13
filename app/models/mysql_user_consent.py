# mysql_user_consent.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserConsent(db.Model):
    __tablename__ = 'user_consent'

    user_id = db.Column(db.String(20), db.ForeignKey('login.user_id'), primary_key=True)
    personal_info_consent = db.Column(db.Boolean, nullable=False)
    terms_of_service_consent = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Login', backref='user_consent')

    def __repr__(self):
        return self.user_id
