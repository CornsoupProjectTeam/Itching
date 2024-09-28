from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PublicProfileList(db.Model):
    __tablename__ = 'PUBLIC_PROFILE_LIST'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    profile_image_path = db.Column(db.String(255))
    freelancer_badge = db.Column(db.Enum('Gold', 'Silver', 'Bronze'))
    match_count = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Integer)
    freelancer_registration_date = db.Column(db.DateTime)
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('public_profile_lists', uselist=False, cascade="all, delete-orphan"))
