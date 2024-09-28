from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CareerMapping(db.Model):
    __tablename__ = 'CAREER_MAPPING'
    
    career_id = db.Column(db.String(50), primary_key=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('careers', lazy=True))
