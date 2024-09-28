from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerAccountInfo(db.Model):
    __tablename__ = 'FREELANCER_ACCOUNT_INFO'
    
    account_id = db.Column(db.String(50), primary_key=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False)
    bank_name = db.Column(db.String(50), nullable=False)
    account_number = db.Column(db.String(255), nullable=False)
    account_holder = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.Enum('Personal', 'Corporation'), nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('account_info', uselist=False, cascade="all, delete-orphan"))
