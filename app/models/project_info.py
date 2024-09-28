from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProjectInfo(db.Model):
    __tablename__ = 'PROJECT_INFO'
    
    project_id = db.Column(db.String(50), primary_key=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False) 
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code', ondelete='CASCADE'), nullable=False) 
    project_title = db.Column(db.String(200), nullable=False)
    project_payment_amount = db.Column(db.Integer, nullable=False)
    design_draft_count = db.Column(db.Integer, nullable=False)
    production_time = db.Column(db.Integer, nullable=False)
    commercial_user_allowed = db.Column(db.Boolean, default=False)
    high_resolution_file_available = db.Column(db.Boolean, default=False)
    delivery_routes = db.Column(db.Text)
    additional_notes = db.Column(db.Text)
    cancellation_and_refund_policy = db.Column(db.Text)
    product_info_disclosure = db.Column(db.Text)
    additional_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('projects_info', lazy=True, cascade="all, delete-orphan"))
    field_keywords = db.relationship('FieldKeywords', backref=db.backref('projects', lazy=True, cascade="all, delete-orphan"))
