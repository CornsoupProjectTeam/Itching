from sqlalchemy.orm import relationship, backref
from datetime import datetime
from app import db

# UserInformation 모델
class UserInformation(db.Model):  # db.Model 상속
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
    
    login = db.relationship('Login', backref=backref('user_information', uselist=False, cascade="all, delete-orphan"))

# ClientPreferredFieldMapping 모델
class ClientPreferredFieldMapping(db.Model):  # db.Model 상속
    __tablename__ = 'CLIENT_PREFERRED_FIELD_MAPPING'
    
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), primary_key=True)
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code', ondelete='CASCADE'), primary_key=True)
    
    user = db.relationship('UserInformation', backref=backref('client_preferred_fields', lazy=True, cascade="all, delete-orphan"))
    field_keyword = db.relationship('FieldKeywords', backref=backref('client_preferred_fields', lazy=True, cascade="all, delete-orphan"))

# PreferredFreelancerMapping 모델
class PreferredFreelancerMapping(db.Model):  # db.Model 상속
    __tablename__ = 'PREFERRED_FREELANCER_MAPPING'
    
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), primary_key=True)  
    preferred_code = db.Column(db.String(20), db.ForeignKey('PREFERRED_KEYWORDS.preferred_code', ondelete='CASCADE'), primary_key=True)
    
    user = db.relationship('UserInformation', backref=backref('preferred_freelancers', lazy=True, cascade="all, delete-orphan"))
    preferred_keyword = db.relationship('PreferredKeywords', backref=backref('preferred_freelancers', lazy=True, cascade="all, delete-orphan"))
