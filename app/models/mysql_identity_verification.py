# mysql_identity_verification.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class IdentityVerification(db.Model):
    __tablename__ = 'IDENTITY_VERIFICATION'

    user_id = db.Column(db.String(20), db.ForeignKey('LOGIN.user_id'), primary_key=True)
    verification_status = db.Column(db.Boolean, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    verification_code = db.Column(db.String(6), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('LOGIN', backref='identity_verification')

    def __repr__(self):
        return self.user_id
