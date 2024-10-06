from app import db

class SkillKeywords(db.Model):
    __tablename__ = 'SKILL_KEYWORDS'
    
    skill_code = db.Column(db.String(20), primary_key=True)
    skill_name = db.Column(db.String(100), unique=True, nullable=False)
