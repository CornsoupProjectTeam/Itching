from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerServiceOptions(db.Model):
    __tablename__ = 'FREELANCER_SERVICE_OPTIONS'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    weekend_consultation = db.Column(db.Boolean, default=False)
    weekend_work = db.Column(db.Boolean, default=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('service_options', uselist=False, cascade="all, delete-orphan"))