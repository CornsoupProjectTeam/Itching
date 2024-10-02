from app import db
from datetime import datetime

class UserConsent(db.Model):
    __tablename__ = 'USER_CONSENT'
    
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), primary_key=True)
    personal_info_consent = db.Column(db.Boolean, nullable=False, default=False)
    terms_of_service_consent = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('UserInformation', backref=db.backref('user_consents', uselist=False, cascade="all, delete-orphan"))
