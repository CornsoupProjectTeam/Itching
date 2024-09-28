from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ReviewSummary(db.Model):
    __tablename__ = 'REVIEW_SUMMARY'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    total_reviews = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('review_summary', uselist=False, cascade="all, delete-orphan"))
