from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProjectList(db.Model):
    __tablename__ = 'PROJECT_LIST'
    
    project_id = db.Column(db.String(50), db.ForeignKey('PROJECT_INFO.project_id', ondelete='CASCADE'), primary_key=True) 
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False) 
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code', ondelete='CASCADE')) 
    project_title = db.Column(db.String(200), nullable=False)
    project_payment_amount = db.Column(db.Integer, nullable=False)
    avg_response_time = db.Column(db.Integer)
    freelancer_badge = db.Column(db.Enum('Gold', 'Silver', 'Bronze'))
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    weekend_consultation = db.Column(db.Boolean, default=False)
    weekend_work = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project_info = db.relationship('ProjectInfo', backref=db.backref('project_list', uselist=False, cascade="all, delete-orphan"))
    public_profile = db.relationship('PublicProfile', backref=db.backref('project_lists', lazy=True, cascade="all, delete-orphan"))
    field_keywords = db.relationship('FieldKeywords', backref=db.backref('project_lists', lazy=True, cascade="all, delete-orphan"))
