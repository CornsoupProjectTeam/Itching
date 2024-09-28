from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FreelancerCareerMapping(db.Model):
    __tablename__ = 'FREELANCER_CAREER_MAPPING'
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('careers', lazy=True, cascade="all, delete-orphan"))
