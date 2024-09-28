from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerExpertiseFieldMapping(db.Model):
    __tablename__ = 'FREELANCER_EXPERTISE_FIELD_MAPPING'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code', ondelete='CASCADE'))
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('expertise_fields', lazy=True, cascade="all, delete-orphan"))
    field_keywords = db.relationship('FieldKeywords', backref=db.backref('freelancer_expertise_mappings', lazy=True, cascade="all, delete-orphan"))
