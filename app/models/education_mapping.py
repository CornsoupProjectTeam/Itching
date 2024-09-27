from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EducationMapping(db.Model):
    __tablename__ = 'EDUCATION_MAPPING'
    
    education_id = db.Column(db.String(50), primary_key=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('educations', lazy=True))
