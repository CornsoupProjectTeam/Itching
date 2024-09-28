from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerSkillMapping(db.Model):
    __tablename__ = 'FREELANCER_SKILL_MAPPING'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    skill_code = db.Column(db.String(20), db.ForeignKey('SKILL_KEYWORDS.skill_code', ondelete='CASCADE'), primary_key=True)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('skills', lazy=True, cascade="all, delete-orphan"))
    skill_keywords = db.relationship('SkillKeywords', backref=db.backref('freelancer_skills_mappings', lazy=True, cascade="all, delete-orphan"))
