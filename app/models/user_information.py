from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserInformation(db.Model):
    __tablename__ = 'USER_INFORMATION'
    
    user_id = db.Column(db.String(20), db.ForeignKey('LOGIN.user_id', ondelete='CASCADE'), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_picture_path = db.Column(db.String(255))
    nickname = db.Column(db.String(20), nullable=False)
    business_area = db.Column(db.String(100))
    inquiry_st = db.Column(db.Boolean, default=False)
    freelancer_registration_st = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    login = db.relationship('Login', backref=db.backref('user_information', uselist=False, cascade="all, delete-orphan"))
