from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PublicProfile(db.Model):
    __tablename__ = 'PUBLIC_PROFILE'
    
    public_profile_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    profile_image_path = db.Column(db.String(255))
    freelancer_intro_one_liner = db.Column(db.String(100))
    freelancer_intro = db.Column(db.Text)
    project_duration = db.Column(db.Integer)
    freelancer_badge = db.Column(db.Enum('Gold', 'Silver', 'Bronze'), default='Bronze')
    match_count = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Integer)
    freelancer_registration_date = db.Column(db.DateTime)
    public_profile_registration_st = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('public_profiles', lazy=True, cascade="all, delete-orphan"))
