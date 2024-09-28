from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerEducationMapping(db.Model):
    __tablename__ = 'FREELANCER_EDUCATION_MAPPING' 
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('educations', lazy=True, cascade="all, delete-orphan"))
