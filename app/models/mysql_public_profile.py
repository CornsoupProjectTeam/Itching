# mysql_public_profile.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PublicProfile(db.Model):
    __tablename__ = 'PUBLIC_PROFILE'

    public_profile_id = db.Column(db.String(30), primary_key=True)
    freelancer_user_id = db.Column(db.String(20), db.ForeignKey('LOGIN.user_id'), nullable=False)
    profile_image_path = db.Column(db.String(255), nullable=True)
    nickname = db.Column(db.String(20), nullable=False)
    matching_count = db.Column(db.Integer, default=0)
    service_option = db.Column(db.Text, nullable=True)
    avg_response_time = db.Column(db.Integer, nullable=True)
    price_unit = db.Column(db.String(5), nullable=True)
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False)
    specialization = db.Column(db.String(255), nullable=True)
    avg_rating = db.Column(db.Numeric(3, 1), nullable=True)
    freelancer_badge = db.Column(db.String(10), nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    freelancer = db.relationship('LOGIN', backref='public_profiles')

    def __repr__(self):
        return self.public_profile_id
