from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerPortfolioMapping(db.Model):
    __tablename__ = 'FREELANCER_PORTFOLIO_MAPPING'  
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('portfolios', cascade="all, delete-orphan", lazy=True))
    
