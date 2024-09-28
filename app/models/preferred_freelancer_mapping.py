from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PreferredFreelancerMapping(db.Model):
    __tablename__ = 'PREFERRED_FREELANCER_MAPPING'
    
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id'), primary_key=True)
    preferred_code = db.Column(db.String(20), db.ForeignKey('PREFERRED_KEYWORDS.preferred_code'))
    
    user = db.relationship('UserInformation', backref=db.backref('preferred_freelancers', lazy=True))
    preferred_keyword = db.relationship('PreferredKeywords', backref=db.backref('preferred_freelancers', lazy=True))
