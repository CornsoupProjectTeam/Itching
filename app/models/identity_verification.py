from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class IdentityVerification(db.Model):
    __tablename__ = 'IDENTITY_VERIFICATION'
    
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), primary_key=True)
    verification_st = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(20), nullable=False)
    verification_code = db.Column(db.String(6), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('UserInformation', backref=db.backref('identity_verifications', uselist=False, cascade="all, delete-orphan"))
