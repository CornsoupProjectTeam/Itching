from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Recommendation(db.Model):
    __tablename__ = 'RECOMMENDATION'
    
    recommendation_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id'), nullable=False)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id'), nullable=False)
    match_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('UserInformation', backref=db.backref('recommendations', lazy=True))
    public_profile = db.relationship('PublicProfile', backref=db.backref('recommendations', lazy=True))
