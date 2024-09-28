from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PostManagement(db.Model):
    __tablename__ = 'POST_MANAGEMENT'
    
    post_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.Enum('Client', 'Project'), nullable=False)
    reference_post_id = db.Column(db.String(50), nullable=False)
    project_title = db.Column(db.String(200), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('post_managements', lazy=True, cascade="all, delete-orphan"))
