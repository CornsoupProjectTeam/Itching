from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerSkillsMapping(db.Model):
    __tablename__ = 'FREELANCER_SKILLS_MAPPING'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id'), primary_key=True)
    skill_code = db.Column(db.String(20), db.ForeignKey('SKILL_KEYWORDS.skill_code'))
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('skills', lazy=True))
    skill_keywords = db.relationship('SkillKeywords', backref=db.backref('freelancer_skills_mappings', lazy=True))
