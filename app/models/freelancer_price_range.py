from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FreelancerPriceRange(db.Model):
    __tablename__ = 'FREELANCER_PRICE_RANGE'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id'), primary_key=True)
    min_price = db.Column(db.Numeric(10, 2), nullable=False)
    max_price = db.Column(db.Numeric(10, 2), nullable=False)
    price_unit = db.Column(db.Enum('KRW', 'USD'), default='KRW')
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('price_range', uselist=False))
